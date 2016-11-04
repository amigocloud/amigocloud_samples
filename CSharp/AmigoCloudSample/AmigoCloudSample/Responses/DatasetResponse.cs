using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AmigoCloudSample.Responses
{
    internal class DatasetResponse
    {
        public int id { get; set; }
        public string url { get; set; }
        public string project { get; set; }
        public string name { get; set; }
        public string table_name { get; set; }
        public bool visible { get; set; }
        public string schema { get; set; }
        public string geometry_column { get; set; }
        public string description { get; set; }
        public string created_on { get; set; }
        public string last_updated { get; set; }
        public string type { get; set; }
        public string geo_type { get; set; }
        public string wkt_geo_type { get; set; }
        public int feature_count { get; set; }
        public string boundingbox { get; set; }
        public string style { get; set; }
        public string forms { get; set; }
        public string preview_image { get; set; }
        public string tiles { get; set; }
        public string preview { get; set; }
        public string preview_vector { get; set; }
        public string notifications { get; set; }
        public string states { get; set; }
        public string master { get; set; }
        public string changeset { get; set; }
        public string export { get; set; }
        public string submit_change { get; set; }
        public string generalization { get; set; }
        public string related_tables { get; set; }

        public string relationships { get; set; }

        public override string ToString()
        {
            return name;
        }
    }
}
