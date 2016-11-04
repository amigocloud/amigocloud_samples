using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AmigoCloudSample
{
    public class AmigoCloudRestSharpOAuth2Authenticator : RestSharp.Authenticators.OAuth2Authenticator
    {

        public AmigoCloudRestSharpOAuth2Authenticator(string access_token)
            : base(access_token)
        {
        }

        public override void Authenticate(RestSharp.IRestClient client, RestSharp.IRestRequest request)
        {
            bool foundAuthorizationHeader = false;

            for (int i = 0; i < request.Parameters.Count; i++)
            {
                if (request.Parameters[i].Name == "Authorization")
                {
                    foundAuthorizationHeader = true;
                    break;
                    // do nothing
                }
            }

            if (foundAuthorizationHeader)
            {
                // do nothing
            }
            else
            {
                request.AddHeader("Authorization", "Bearer " + base.AccessToken);
            }
            // curl --header "Authorization: Bearer tDmfUNoKehyiIH2JK2inUCySzM8AWu" http://qa-amigocloud.urbanfootprint.net/footprint/amigocloud/gptool_data/


        }
    }

}
