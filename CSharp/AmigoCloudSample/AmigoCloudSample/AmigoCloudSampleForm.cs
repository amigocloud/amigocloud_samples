using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using AmigoCloudSample.Responses;

namespace AmigoCloudSample
{
    public partial class AmigoCloudSampleForm : Form
    {

        private RestSharp.IRestClient m_clientConnection = null;
        public AmigoCloudSampleForm()
        {
            InitializeComponent();
        }
    

        private void LoginButton_Click(object sender, EventArgs e)
        {

            if ( String.IsNullOrEmpty( EmailTextBox.Text ) ){
                MessageBox.Show("Please input the email for your account");
                return;
            }

            if (String.IsNullOrEmpty(PasswordTextBox.Text))
            {
                MessageBox.Show("Please input the password for your account");
                return;
            }

            // Login

            Uri amigoCloudServer = new Uri("https://app.amigocloud.com/api/v1/");
            string clientId = "510cf3891778c5f6587e";
            string clientSecret = "f59e18e727c84c6ed108e59bc519fdbcfd07ecbb";

            m_clientConnection = AmigoCloudServerUtilities.Server_LoginHelper(amigoCloudServer, clientId, clientSecret, EmailTextBox.Text, PasswordTextBox.Text, "oauth2/access_token");

            // Populate the projects combo box.

            ProjectsResponse projects = AmigoCloudServerUtilities.Server_GetAllVisibleProjects( m_clientConnection );

            foreach ( ProjectResponse currentProject in projects.results ){
                ProjectsComboBox.Items.Add(currentProject );
            }

            LoginGroupBox.Enabled = false;
            SelectDatasetGroupBox.Enabled = true;
            DatasetsComboBox.Enabled = false;

        }

        private void ProjectsComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            DatasetsComboBox.Items.Clear();

            DatasetsResponse datasets = AmigoCloudServerUtilities.Server_GetDatasets(m_clientConnection, ProjectsComboBox.SelectedItem as ProjectResponse);
            
            foreach (DatasetResponse currentDataset in datasets.results)
            {
                if ( currentDataset.type == "vector"){
                    DatasetsComboBox.Items.Add(currentDataset);
                }
            }

            DatasetsComboBox.Enabled = true;

        }

        private void DatasetsComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {

            ProjectResponse selectedProject = ProjectsComboBox.SelectedItem as ProjectResponse;
            DatasetResponse selectedDataset = DatasetsComboBox.SelectedItem as DatasetResponse;

            string query = "SELECT * from " + selectedDataset.table_name + " LIMIT 100";

            SqlQueryResponse queryResponse = AmigoCloudServerUtilities.Server_QueryDataset( m_clientConnection, selectedProject, selectedDataset, query );

            DatasetDataGridView.Columns.Clear();
            DatasetDataGridView.ColumnCount = queryResponse.columns.Count;

            for ( int i = 0; i < queryResponse.columns.Count ; i++){

                DatasetDataGridView.Columns[i].Name = queryResponse.columns[i].name;

            }

            foreach (var currentRow in queryResponse.data)
            {

                List<string> currentRowData = new List<string>();
                foreach (var fieldItem in currentRow.KeyValueList)
                {
                    currentRowData.Add( Utilities.Safe_ObjectToString( fieldItem.value ) );
                }

                DatasetDataGridView.Rows.Add(currentRowData.ToArray());

            }


        }






    }
}
