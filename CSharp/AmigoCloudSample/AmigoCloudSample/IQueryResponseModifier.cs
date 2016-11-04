using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AmigoCloudSample
{
    public interface IQueryResponseModifier
    {
        string ModifyContent(string content);
    }
}
