using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AmigoCloudSample.Responses
{
    public class SqlQueryResponse
    {

        public string query { get; set; }
        public int count { get; set; }
        public int limit { get; set; }
        public int offset { get; set; }

        public List<SqlQueryColumn> columns { get; set; }
        public List<AnonymousList> data { get; set; }

        public void AppendQuery(SqlQueryResponse additionalQuery)
        {

            // count is the same
            // query is the same
            // limit is different
            limit += additionalQuery.limit;
            // offset is the same
            // columns is the same
            data.AddRange(additionalQuery.data);

        }

        public string new_state { get; set; }

    }

    public class SqlQueryColumn
    {
        public string type { get; set; }
        public string name { get; set; }
        public int? max_length { get; set; }
    }


    public class CustomKeyValuePair
    {
        public string key { get; set; }
        public object value { get; set; }
    }

    public class AnonymousList
    {
        public List<CustomKeyValuePair> KeyValueList;
    }
}
