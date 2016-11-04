using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using AmigoCloudSample.Responses;
using AmigoCloudSample.Exceptions;
using AmigoCloudSample.ResponseModifiers;

namespace AmigoCloudSample
{
    class AmigoCloudServerUtilities
    {
        /// <summary>
        /// Exceptions: 
        /// RestSharpException - Error communicating with the server. 
        /// </summary>
        /// <param name="uri"></param>
        /// <param name="clientId"></param>
        /// <param name="clientSecret"></param>
        /// <param name="email"></param>
        /// <param name="password"></param>
        /// <param name="oauthEndpoint"></param>
        /// <returns></returns>
        public static RestSharp.IRestClient Server_LoginHelper(Uri uri, string clientId, string clientSecret, string email, string password, string oauthEndpoint)
        {

            RestSharp.IRestClient client = new RestSharp.RestClient(uri) as RestSharp.IRestClient;

            RestSharp.RestRequest request = new RestSharp.RestRequest(RestSharp.Method.POST);
            request.Resource = oauthEndpoint; 
            request.AddParameter("client_id", clientId);
            request.AddParameter("client_secret", clientSecret);
            request.AddParameter("grant_type", "password");
            request.AddParameter("username", email);
            request.AddParameter("password", password);

            try
            {


                Responses.AuthenticationResponse authResponse = RestSharpUtilities.ExecuteRequest<AuthenticationResponse>(client, request);

                RestSharpUtilities.LoginTime = DateTime.Now;
                RestSharpUtilities.AccessToken = authResponse.access_token;
                RestSharpUtilities.TokenLifespanSeconds = authResponse.expires_in;
                RestSharpUtilities.ClientId = clientId;
                RestSharpUtilities.ClientSecret = clientSecret;
                RestSharpUtilities.RefreshToken = authResponse.refresh_token;

                client.Authenticator = new AmigoCloudRestSharpOAuth2Authenticator(authResponse.access_token);

                return client;

            }
            catch (RestSharpException e)
            {
                // unable to login or something...
                System.Diagnostics.Trace.WriteLine(e.ToString());
                throw;
            }

        } // Server_LoginHelper


        /// <summary>
        /// Will return a projects response will all visible projects. This will iterate through all pages to return
        /// a list of all visible project
        /// </summary>
        /// <exception cref="ArgumentException">It will return an argument exception if there is no connection to the AmigoCloud Server.</exception>
        /// <param name="acConnection"></param>
        /// <returns></returns>
        internal static ProjectsResponse Server_GetAllVisibleProjects(RestSharp.IRestClient clientConnection )
        {

            if (null == clientConnection)
            {
                throw new ArgumentNullException("The input client is null");
            }

            string requestUrl = "me" + "/projects";

            // get the first page... 
            ProjectsResponse returnList = RestSharpUtilities.ExecuteRequest<ProjectsResponse>(clientConnection, requestUrl, RestSharp.Method.GET);

            // start checking next pages
            while (returnList.next != null)
            {

                string nextUrl = RestSharpUtilities.Client_TrimUrl(clientConnection, returnList.next);
                ProjectsResponse nextPageOfProjects = RestSharpUtilities.ExecuteRequest<ProjectsResponse>(clientConnection, nextUrl, RestSharp.Method.GET);

                returnList.next = nextPageOfProjects.next;
                returnList.results.AddRange(nextPageOfProjects.results);
                returnList.count += nextPageOfProjects.count;

            }

            return returnList;

        }


        /// <summary>
        /// This function will retrieve the list of datasets for the specified project. 
        /// </summary>
        /// <param name="client">The client connection to the amigo cloud server.</param>
        /// <param name="projectId">The id of the project to get the datasets from.</param>
        /// <returns>A datasets response which may contain 0 or more datasetresponses depending on whether or not the project has any datasets. </returns>
        internal static DatasetsResponse Server_GetDatasets(RestSharp.IRestClient clientConnection, ProjectResponse project )
        {

            string url = RestSharpUtilities.Client_TrimUrl(clientConnection, project.datasets);

            DatasetsResponse returnDatasets = new DatasetsResponse();


            DatasetsResponse currentDatasets = RestSharpUtilities.ExecuteRequest<DatasetsResponse>(clientConnection, url, RestSharp.Method.GET);
            returnDatasets.results = currentDatasets.results;
            returnDatasets.count = currentDatasets.count;

            while (null != currentDatasets.next)
            {

                string nextUrl = currentDatasets.next;
                string trimmedUrl = RestSharpUtilities.Client_TrimUrl(clientConnection, currentDatasets.next);
                currentDatasets = RestSharpUtilities.ExecuteRequest<DatasetsResponse>(clientConnection, trimmedUrl, RestSharp.Method.GET);

                // append to the return datasets
                returnDatasets.results.AddRange(currentDatasets.results);
                returnDatasets.count += currentDatasets.count;
                returnDatasets.next = currentDatasets.next;

            }

            return returnDatasets;

        }


        internal static SqlQueryResponse Server_QueryDataset(RestSharp.IRestClient clientConnection, ProjectResponse project, DatasetResponse dataset, string sqlQuery)
        {
            
            string url = RestSharpUtilities.Client_TrimUrl(clientConnection, project.sql);

            RestSharp.Method method = RestSharp.Method.GET;

            if (sqlQuery.ToUpper().Contains("INSERT"))
            {
                return null;
            }
            else if (sqlQuery.ToUpper().Contains("UPDATE"))
            {
                return null;
            }
            else if (sqlQuery.ToUpper().Contains("DELETE"))
            {
                return null;
            }
            else
            {
                method = RestSharp.Method.GET;
            }

            RestSharp.IRestRequest request = new RestSharp.RestRequest(url, method);

            request.AddParameter("query", sqlQuery);

            if (-1 == dataset.id)
            {
                // do nothing
            }
            else
            {

                request.AddParameter("dataset_id", dataset.id.ToString());

            }


            SqlQueryResponse response = RestSharpUtilities.ExecuteRequest<SqlQueryResponse>(clientConnection, request, new SqlQueryResponseModifier());

            return response;

        } // Server_QueryDataset

    }
}
