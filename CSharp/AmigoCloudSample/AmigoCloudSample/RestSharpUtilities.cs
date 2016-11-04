using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using AmigoCloudSample.Responses;
using AmigoCloudSample.Exceptions;

namespace AmigoCloudSample
{
    public class RestSharpUtilities
    {

        public static DateTime LoginTime { get; set; }
        public static string RefreshToken { get; set; }
        public static string AccessToken { get; set; }
        public static int TokenLifespanSeconds { get; set; }
        public static string ClientSecret { get; set; }
        public static string ClientId { get; set; }

        private static bool RefreshTokenIfNeeded(RestSharp.IRestClient client)
        {

            if (LoginTime.Equals(new DateTime()))
            {
                return false;
            }

            TimeSpan fiveMinutes = new TimeSpan(0, 55, 0);

            DateTime ExpiredTime = LoginTime.AddSeconds(TokenLifespanSeconds).Subtract(fiveMinutes);

            // Utilities.WriteDebugMessage("Expired Time : " + Utilities.Date_ConvertToString( ExpiredTime );
            // Utilities.WriteDebugMessage("Login Time : " + Utilities.Date_ConvertToString( LoginTime );
            // Utilities.WriteDebugMessage("Now : " + Utilities.Date_ConvertToString(DateTime.Now));

            if (DateTime.Now > ExpiredTime)
            {

                // refresh the token
                RestSharp.RestRequest request = new RestSharp.RestRequest(RestSharp.Method.POST);
                request.Resource = "oauth2/access_token";
                request.AddParameter("client_id", RestSharpUtilities.ClientId);
                request.AddParameter("client_secret", RestSharpUtilities.ClientSecret);
                request.AddParameter("grant_type", "refresh_token");
                request.AddParameter("refresh_token", RestSharpUtilities.RefreshToken);


                RestSharpUtilities.LoginTime = DateTime.Now; // set this here to avoid stack overflow. 

                AuthenticationResponse authResponse = RestSharpUtilities.ExecuteRequest<AuthenticationResponse>(client, request);

                RestSharpUtilities.AccessToken = authResponse.access_token;
                RestSharpUtilities.TokenLifespanSeconds = authResponse.expires_in;
                RestSharpUtilities.RefreshToken = authResponse.refresh_token;

                client.Authenticator = new AmigoCloudRestSharpOAuth2Authenticator(authResponse.access_token);

                return true;

            }
            else
            {
                return false;
            }

        }



        public static RestSharp.IRestResponse ExecuteRequest(RestSharp.IRestClient client, RestSharp.IRestRequest request)
        {

            if (null == request)
            {
                throw new InvalidOperationException("Input request is null");
            }

            if (null == client)
            {
                throw new ArgumentNullException("Input client connection is null");
            }

            RefreshTokenIfNeeded(client);

            bool foundGzip = false;

            foreach (RestSharp.Parameter parameter in request.Parameters)
            {

                if (parameter.Name == "Accept-Encoding")
                {
                    foundGzip = true;
                    parameter.Value = "gzip, deflate";
                }

            }

            request.RequestFormat = RestSharp.DataFormat.Json;


            if (!foundGzip)
            {
                request.AddHeader("Accept-Encoding", "gzip,deflate");
            }

            int djangoServerIsDownCount = 0;
            int noResponseCount = 0;
            RestSharp.IRestResponse rsResponse = null;

            while (true)
            {

                rsResponse = client.Execute(request);

#if DEBUG
                string debugMessage = "Request Information (from request object): " + Environment.NewLine + Request_ToPrintString(request);

                debugMessage += Response_ToStackTrace(rsResponse);

#endif

                int tryCount = 0;

                if (rsResponse.RawBytes != null)
                {

                    while ((rsResponse.ContentLength != rsResponse.RawBytes.LongLength) && tryCount > 0)
                    {
                        rsResponse = client.Execute(request);
                        tryCount--;

                        if (tryCount == 0)
                        {
                            throw new InvalidOperationException("The download failed");
                        }

                    }

                }
                else
                {
                    // the server was not availiable so we have no response.
                    if (noResponseCount > 3)
                    {
                        // do nothing
                    }
                    else
                    {
                        noResponseCount++;
                        continue;
                    }

                }

                if (rsResponse.StatusCode == 0)
                {
                    // bad error! 
                    throw new RestSharpException(rsResponse, rsResponse.ErrorException);

                }
                else if (rsResponse.StatusCode == System.Net.HttpStatusCode.OK)
                {
                    // this is fine
                }
                else if (rsResponse.StatusCode == System.Net.HttpStatusCode.Created)
                {
                    // this is fine
                }
                else if (rsResponse.StatusCode == System.Net.HttpStatusCode.NoContent)
                {
                    // this is fine, usually a successful delete
                }
                else if (rsResponse.StatusCode == System.Net.HttpStatusCode.Accepted)
                {
                    // this is fine
                }
                else if (rsResponse.StatusCode == System.Net.HttpStatusCode.NonAuthoritativeInformation)
                {
                    // this is fine
                }
                else if (rsResponse.StatusCode == System.Net.HttpStatusCode.ResetContent)
                {
                    // this is fine
                }
                else if (rsResponse.StatusCode == System.Net.HttpStatusCode.PartialContent)
                {
                    // this is fine
                }
                else if (429 == (int)rsResponse.StatusCode)
                {

                    // too many requests... we need to pause and wait for the server to catch up. 
                    // I put 10 min total and that is pretty darn excessive
                    if (djangoServerIsDownCount > 20)
                    {
                        throw new RestSharpException(rsResponse);
                    }
                    else
                    {
                        System.Threading.Thread.Sleep(30000);
                        djangoServerIsDownCount++;
                        continue;
                    }

                }
                else if ((rsResponse.StatusCode == System.Net.HttpStatusCode.BadGateway) | (rsResponse.StatusCode == System.Net.HttpStatusCode.GatewayTimeout))
                {

                    if (rsResponse.Server.ToLower().Contains("nginx"))
                    {

                        if (djangoServerIsDownCount > 30)
                        {
                            throw new RestSharpException(rsResponse);
                        }
                        else
                        {

                            // the server is returning a bad gateway or gateway timeout from django... this happens during a restart of the server or if the django server is too busy...
                            // we should wait 5 seconds and retry...
                            System.Threading.Thread.Sleep(10000);
                            djangoServerIsDownCount++;
                            continue;

                        }

                    }
                    else
                    {
                        throw new RestSharpException(rsResponse);
                    }

                }
                else
                {

                    throw new RestSharpException(rsResponse);
                }

                // no errors, we must have a good response break out of the loop. 
                break;

            }

            return rsResponse;

        }


        private static T DeserializeContent<T>(string content, IQueryResponseModifier responseModifier = null)
        {

            // use this to capture resposnes before modification.
            // System.IO.File.WriteAllText(Globals.ErrorDirectory + "Response - " + Utilities.Date_ConvertToString( DateTime.Now ) + ".txt", "Origional Content: " + content);


            T deserializedObject = default(T);
            string modifiedContent = "";

            try
            {
                if (null == responseModifier)
                {
                    deserializedObject = Newtonsoft.Json.JsonConvert.DeserializeObject<T>(content);
                }
                else
                {
                    modifiedContent = responseModifier.ModifyContent(content);
                    Newtonsoft.Json.JsonSerializerSettings settings = new Newtonsoft.Json.JsonSerializerSettings();
                    settings.DateFormatHandling = Newtonsoft.Json.DateFormatHandling.IsoDateFormat;
                    settings.DateParseHandling = Newtonsoft.Json.DateParseHandling.None;

                    deserializedObject = Newtonsoft.Json.JsonConvert.DeserializeObject<T>(modifiedContent, settings);
                }
            }
            catch (Exception)
            {
                throw;
            }

            return deserializedObject;

        }

        public static T ExecuteRequest<T>(RestSharp.IRestClient client, string request, RestSharp.Method method, IQueryResponseModifier responseModifier = null)
        {
            RestSharp.IRestRequest rsRequest = new RestSharp.RestRequest(request, method);
            return ExecuteRequest<T>(client, rsRequest, responseModifier);

        }

        public static T ExecuteRequest<T>(RestSharp.IRestClient client, RestSharp.IRestRequest request, IQueryResponseModifier responseModifier = null)
        {

            if (null == request)
            {
                throw new InvalidOperationException("Input request is null");
            }

            RestSharp.IRestResponse response = ExecuteRequest(client, request);
            return DeserializeContent<T>(response.Content, responseModifier);

        }


        private static string Request_ToPrintString(RestSharp.IRestRequest request)
        {

            string stackTrace = "";
            string indent = "    ";

            if (null == request)
            {
                // occurs when the server is bad. 
                stackTrace += indent + "[The input request was null]" + Environment.NewLine;
            }
            else
            {
                stackTrace += indent + "Resource: " + request.Resource + Environment.NewLine;
                stackTrace += indent + "Method: " + request.Method.ToString() + Environment.NewLine;

                stackTrace += indent + "Parameters: " + Environment.NewLine;
                for (int i = 0; i < request.Parameters.Count; i++)
                {
                    stackTrace += indent + indent + "Parameter [" + request.Parameters[i].Name + "] = " + Utilities.Safe_ObjectToString(request.Parameters[i].Value) + Environment.NewLine;
                }

                stackTrace += indent + "Files: " + Environment.NewLine;

                if (request.Files.Count > 0)
                {
                    for (int i = 0; i < request.Files.Count; i++)
                    {
                        stackTrace += indent + indent + "File [" + request.Files[i].FileName + "] = (" + request.Files[i].ContentType + ", " + request.Files[i].ContentLength.ToString() + " ) " + Environment.NewLine;
                    }
                }
                else
                {
                    stackTrace += indent + indent + "No Files" + Environment.NewLine;
                }
            }

            return stackTrace;

        }



        internal static string Response_ToStackTrace(RestSharp.IRestResponse response)
        {

            string indent = "    ";

            string stackTrace = "Request Information (From Response Object): " + Environment.NewLine;

            stackTrace += Request_ToPrintString(response.Request);

            stackTrace += "Response Information: " + Environment.NewLine;

            stackTrace += indent + "Headers:" + Environment.NewLine;

            for (int i = 0; i < response.Headers.Count; i++)
            {
                stackTrace += indent + indent + "Header: [" + response.Headers[i].Name + "] = " + response.Headers[i].Value.ToString() + Environment.NewLine;
            }

            // stackTrace += indent + "Content (trimmed ): " + response.Content.Substring(0, response.Content.Length > 1000 ? 1000 : response.Content.Length) + Environment.NewLine;
            if (String.IsNullOrEmpty(response.Content))
            {
                stackTrace += indent + "Content : " + response.Content + Environment.NewLine;
            }
            else
            {

                stackTrace += indent + "Content : " + Environment.NewLine;

                try
                {

                    string temp = Newtonsoft.Json.Linq.JObject.Parse(response.Content).ToString();
                    temp = indent + temp.Replace(Environment.NewLine, Environment.NewLine + indent) + Environment.NewLine;
                    stackTrace += temp;

                }
                catch (System.OutOfMemoryException)
                {
                    stackTrace += indent + "Unable to parse json to a string. Ran out of memory";

                }
                catch (Newtonsoft.Json.JsonReaderException)
                {
                    stackTrace += indent + "Unable to parse json" + Environment.NewLine;
                    stackTrace += indent + "Json: " + response.Content + Environment.NewLine;
                }


            }

            stackTrace += indent + "Status Code: " + response.StatusCode + Environment.NewLine;
            stackTrace += indent + "Status: " + response.ResponseStatus + Environment.NewLine;
            stackTrace += indent + "Error Exception: " + Utilities.Exception_GetAsPrintString(response.ErrorException) + Environment.NewLine;
            stackTrace += indent + "Error Message: " + response.ErrorMessage + Environment.NewLine;
            stackTrace += indent + "Description: " + response.StatusDescription + Environment.NewLine;
            stackTrace += indent + "Server: " + response.Server + Environment.NewLine;
            stackTrace += indent + Environment.NewLine;
            stackTrace += indent + "Client Stack Trace: " + Environment.NewLine;
            stackTrace += indent + System.Environment.StackTrace;

            return stackTrace;

        }


        internal static string Response_ToString(RestSharp.IRestResponse response)
        {

            string returnValue = "";
            returnValue += "Rest Sharp Exception: " + Environment.NewLine;
            if (null == response.ResponseUri)
            {
                returnValue += "  Absolute Uri: " + "null" + Environment.NewLine;
            }
            else
            {
                returnValue += "  Absolute Uri: " + response.ResponseUri.AbsoluteUri + Environment.NewLine;
            }

            returnValue += "  Content: " + response.Content + Environment.NewLine;
            returnValue += "  Status: " + response.ResponseStatus + Environment.NewLine;

            return returnValue;

        }




        /// <summary>
        /// Many of the urls specified by the server, have the server address already in them. To use the url in 
        /// a rest request for rest sharp, you have to trim off the server address, as rest sharp prepends the
        /// baseurl to the request url. 
        /// 
        /// in other words: http://beta.amigocloud.com/api/v1/users/3/projects/123/chunked_uploads
        /// will become: /users/3/projects/123/chunked_uploads
        /// 
        /// </summary>
        /// <param name="client">The client connection to the server</param>
        /// <param name="url">The url from the server.</param>
        /// <returns></returns>
        internal static string Client_TrimUrl(RestSharp.IRestClient client, string url)
        {
            return (url.Substring(client.BaseUrl.AbsoluteUri.Length));
        }



        internal static string Client_GetHostName(RestSharp.IRestClient clientConnection)
        {
            return clientConnection.BaseUrl.Host;
        }

        internal static string DownloadFile(RestSharp.IRestClient restClient, string downloadFilePath, string fileName)
        {


            string tempFile = System.IO.Path.GetTempFileName();

            using (var writer = System.IO.File.OpenWrite(tempFile))
            {
                RestSharp.RestClient client = restClient as RestSharp.RestClient;

                if (null == client)
                {
                    throw new InvalidOperationException("Unable to cast the IRestClient back to restClient");
                }

                string trimmedUrl = Client_TrimUrl(restClient, downloadFilePath);

                var request = new RestSharp.RestRequest(trimmedUrl);
                request.ResponseWriter = (responseStream) => responseStream.CopyTo(writer);
                var response = client.DownloadData(request);
            }

            return tempFile;

        }
    }// Rest Sharp Utilities

} // AmigoCloud Sample Namespace
