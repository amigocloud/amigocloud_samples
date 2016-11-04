using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AmigoCloudSample.ResponseModifiers
{
    public class SqlQueryResponseModifier : IQueryResponseModifier
    {
        /// <summary>
        /// Takes the column information from the sql query response and makes
        /// the columns a json list of objects that have a name and a type. This 
        /// makes it possible to deserialize into a ColumnType rather than a JsonObject
        /// </summary>
        /// <param name="content"></param>
        /// <returns></returns>
        public string ModifyContent(string content)
        {

            string temp2 = Utilities.Json_ConvertListObjectsToListOfNamedLists(content, "data");
            return temp2;
        }


    }
}
