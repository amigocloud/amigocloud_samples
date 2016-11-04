using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AmigoCloudSample.Responses
{
    public class AuthenticationResponse
    {
        public string access_token;
        public string refresh_token;
        public int expires_in;
        public string scope;

        public override string ToString()
        {
            return "AuthenticationResponse: (access_token = " + access_token + ", refresh_token = " + refresh_token + ", expires_in = " + expires_in + " seconds, scope = " + scope + " )";
        }
    }


}