using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AmigoCloudSample.Exceptions
{

    public class RestSharpException : Exception
    {

        string m_fullMessage = null;
        string m_stackTrace = null;
        string m_message = null;
        string m_source = null;
        public string ResponseJSON = null;

        public string ResponseStatus { get; private set; }
        public System.Net.HttpStatusCode ResponseStatusCode { get; private set; }
        public string ErrorMessage = "";

        public RestSharpException(RestSharp.IRestResponse response)
        {

            Initialize(response);

        }

        public RestSharpException(RestSharp.IRestResponse response, Exception innerException)
            : base(response.ErrorMessage, innerException)
        {
            Initialize(response);
        }

        private void Initialize(RestSharp.IRestResponse response)
        {

            m_fullMessage = RestSharpUtilities.Response_ToString(response);
            m_stackTrace = RestSharpUtilities.Response_ToStackTrace(response);
            m_message = response.StatusDescription;
            if (response.ResponseUri == null)
            {
                m_source = "null";
            }
            else
            {
                m_source = response.ResponseUri.Scheme + "://" + response.ResponseUri.Host + response.ResponseUri.AbsolutePath;
            }

            ResponseStatus = response.ResponseStatus.ToString();
            ResponseStatusCode = response.StatusCode;

            ErrorMessage = response.ErrorMessage;



            try
            {
                // convert it to an object, and back (to format nicely).
                object testObject = Newtonsoft.Json.JsonConvert.DeserializeObject(response.Content);
                ResponseJSON = Newtonsoft.Json.JsonConvert.SerializeObject(testObject, Newtonsoft.Json.Formatting.Indented);

            }
            catch (Exception)
            {
                ResponseJSON = null;
            }

        }


        public override string Message
        {
            get
            {
                return m_message;
            }
        }


        public override string StackTrace
        {
            get
            {
                return m_stackTrace;
            }
        }


        public override string Source
        {
            get
            {
                return m_source;
            }
            set
            {

            }
        }

        public override string ToString()
        {
            return m_fullMessage;
        }
    }
}
