using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AmigoCloudSample.Responses
{
    public class ProjectResponse
    {
        public int id { get; set; }
        public string url { get; set; }
        public string owner { get; set; }
        public int owner_id { get; set; }
        public string name { get; set; }
        public string description { get; set; }
        public string organization { get; set; }
        public string created_on { get; set; }
        public string last_updated { get; set; }
        public bool public_read { get; set; }
        public bool public_write { get; set; }
        public string preview_image { get; set; }
        public int dataset_count { get; set; }
        public string datasets { get; set; }
        public int temporary_dataset_count { get; set; }
        public string temporary_datasets { get; set; }
        public string upload { get; set; }
        public string chunked_upload { get; set; }
        public string chunked_upload_complete { get; set; }
        public string upload_datasets { get; set; }
        public string chunked_upload_datasets { get; set; }
        public string base_layers { get; set; }
        public string contributors { get; set; }
        public string grant { get; set; }
        public string revoke { get; set; }
        public string leave { get; set; }
        public string invitations { get; set; }
        public string notifications { get; set; }
        public string queries { get; set; }
        public string support_files { get; set; }
        public string sql { get; set; }
        public string create_dataset { get; set; }
        public string create_temporary_dataset { get; set; }
        public string resend_invite { get; set; }
        public string my_permission_level { get; set; }
        public string offline_areas { get; set; }
        public string job { get; set; }

        public override string ToString()
        {
            return name;

        }


    }
}
