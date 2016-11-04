using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AmigoCloudSample.Responses
{
    public class ProjectsResponse
    {

        public int count { get; set; }
        public string next { get; set; }
        public string previous { get; set; }
        public List<ProjectResponse> results { get; set; }

        internal ProjectResponse FindProjectByName_CaseInsensitive(string projectName)
        {
            foreach (ProjectResponse currentProject in results)
            {
                if (currentProject.name.ToLower() == projectName.ToLower())
                {
                    return currentProject;
                }
            }

            return null;

        }

        internal ProjectResponse FindProjectById(int projectId)
        {

            foreach (ProjectResponse currentProject in results)
            {
                if (currentProject.id == projectId)
                {
                    return currentProject;
                }
            }

            return null;

        }


        internal ProjectResponse FindProjectByNameOrId_CaseInsensitive(string projectNameOrId)
        {

            // first try to find it by name
            ProjectResponse foundProject = FindProjectByName_CaseInsensitive(projectNameOrId);

            if (null == foundProject)
            {

                int testProjectId = -1;

                if (int.TryParse(projectNameOrId, out testProjectId))
                {

                    foundProject = FindProjectById(testProjectId);

                }

            }

            return foundProject;

        }
    }

}
