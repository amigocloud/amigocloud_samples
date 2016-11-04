using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace AmigoCloudSample
{
    class Utilities
    {
        /// <summary>
        /// Global format provider for dates and numbers. We need to default to en_US as that is what AmigoCloud is in. 
        /// </summary>
        internal static IFormatProvider en_US_Provider = new CultureInfo("en-US") as IFormatProvider;
        internal static string DateFormatString = "MMM-dd-yyyy hh:mm:ss.ffffff tt";

        internal static string Safe_ObjectToString(object p)
        {
            if (null == p)
            {
                return "";
            }
            else if (p is System.DateTime)
            {
                return Utilities.Date_ConvertToString((DateTime)p);
            }
            else if (p is System.Double)
            {
                return ((System.Double)p).ToString("G15");
            }
            else
            {
                return p.ToString();
            }

        }

        /// <summary>
        /// Convert a datetime object to a string. We're doing this in lots of places, so this will have common formatting for all of them. 
        /// </summary>
        /// <param name="date"></param>
        /// <returns></returns>
        internal static string Date_ConvertToString(DateTime date)
        {
            return date.ToString(DateFormatString, en_US_Provider);
        }


        internal static string Exception_GetAsPrintString(Exception e, bool isInnerException = false, int innerExceptionCount = 0)
        {

            if (null == e)
            {
                return "";
            }


            MethodInfo preserveStackTrace = typeof(Exception).GetMethod("InternalPreserveStackTrace", BindingFlags.Instance | BindingFlags.NonPublic);
            preserveStackTrace.Invoke(e, null);


            string prefix = "";
            for (int i = 0; i < innerExceptionCount; i++)
            {
                prefix += "    ";
            }

            string printMessage = "";

            if (isInnerException)
            {
                printMessage += prefix + "Inner Exception" + Environment.NewLine;
            }
            else
            {
                printMessage += prefix + "Exception Occured" + Environment.NewLine;
            }

            printMessage += prefix + "----------------------------------------------------------------------------------------------------" + Environment.NewLine;
            printMessage += prefix + "Name : " + e.GetType().Name + Environment.NewLine;
            printMessage += prefix + "Message : " + e.Message + Environment.NewLine;
            printMessage += prefix + "Source (object or application that caused the error) : " + e.Source + Environment.NewLine;
            printMessage += prefix + "Target Site (method that threw the exeption) : " + e.TargetSite + Environment.NewLine;


            if (null != (e as COMException))
            {

                COMException comE = e as COMException;
                printMessage += prefix + "Is COM Error: Yes" + Environment.NewLine;
                printMessage += prefix + "HRESULT : " + comE.ErrorCode + Environment.NewLine;

            }
            else
            {
                printMessage += prefix + "Is COM Error: No" + Environment.NewLine;
                printMessage += prefix + "HRESULT : N/A" + Environment.NewLine;
            }

            printMessage += prefix + "CallStack : " + Environment.NewLine;
            printMessage += prefix + e.StackTrace + Environment.NewLine;


            if (null != e.InnerException)
            {
                printMessage += Exception_GetAsPrintString(e.InnerException, true, innerExceptionCount + 1);
            }

            return printMessage;

        } // Exception_GetAsPrintString



        /// <summary>
        /// In json, an object can have a bunch of properties.
        /// 
        /// "object" : [
        ///		{ "key1": "value1", "key2" : "value2", ... }
        ///		{ "key1": "value1", "key2" : "value2", ... }
        ///	]
        ///	
        /// to deserialize this, we need to change it to a name/value pair list
        /// 
        /// "object" : [
        ///		{ "newList" : [ {"key" : "key1", "value" : "value1"}, {"key" : "key2", "value" : "value2"}], ... }
        ///		{ "newList" : [ {"key" : "key1", "value" : "value1"}, {"key" : "key2", "value" : "value2"}], ... }
        ///	]
        ///	
        /// </summary>
        /// <param name="jsonInput"></param>
        /// <param name="nameOfList"></param>
        /// <param name="nameOfNewObject"></param>
        /// <returns></returns>
        static internal string Json_ConvertListObjectsToListOfNamedLists(string jsonInput, string nameOfList, string nameOfNewObject = "KeyValueList")
        {

            Newtonsoft.Json.Linq.JObject rootObject = Newtonsoft.Json.Linq.JObject.Parse(jsonInput);

            foreach (Newtonsoft.Json.Linq.JProperty testProperty in rootObject.Properties())
            {

                if (testProperty.Name.ToUpper() == nameOfList.ToUpper())
                {
                    // found it!
                    Newtonsoft.Json.Linq.JArray arr = testProperty.Value as Newtonsoft.Json.Linq.JArray;

                    if (null == arr)
                    {
                        throw new ArgumentException("The input json contains a object called " + nameOfList + " but it is not a list.");
                    }

                    Newtonsoft.Json.Linq.JArray newArray = new Newtonsoft.Json.Linq.JArray();

                    foreach (Newtonsoft.Json.Linq.JObject obj in arr)
                    {
                        Newtonsoft.Json.Linq.JArray convertedArray = Json_ConvertObjectToPropertyArray(obj);

                        Newtonsoft.Json.Linq.JObject tempObject = new Newtonsoft.Json.Linq.JObject();
                        tempObject.Add(new Newtonsoft.Json.Linq.JProperty(nameOfNewObject, convertedArray));
                        newArray.Add(tempObject);

                    }

                    testProperty.Value = newArray;

                }

            }


            return rootObject.ToString();

        }


        /// <summary>
        /// This function will take a Newtonsoft Json Object and convert it's parameters into an array of key value pairs. 
        /// </summary>
        /// <param name="jObject"></param>
        /// <param name="keyName"></param>
        /// <param name="valueName"></param>
        /// <returns></returns>
        internal static Newtonsoft.Json.Linq.JArray Json_ConvertObjectToPropertyArray(Newtonsoft.Json.Linq.JObject jObject, string keyName = "key", string valueName = "value")
        {



            Newtonsoft.Json.Linq.JArray newArray = new Newtonsoft.Json.Linq.JArray();

            foreach (Newtonsoft.Json.Linq.JProperty propertyToConvert in jObject.Properties())
            {

                string key = propertyToConvert.Name;
                string value = propertyToConvert.Value.ToString();

                Newtonsoft.Json.Linq.JObject tempObject = new Newtonsoft.Json.Linq.JObject();
                tempObject.Add(keyName, key);
                tempObject.Add(valueName, propertyToConvert.Value);

                newArray.Add(tempObject);

            }

            return newArray;

        }


    }
}
