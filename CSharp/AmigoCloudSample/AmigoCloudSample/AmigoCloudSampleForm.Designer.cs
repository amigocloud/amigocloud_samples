namespace AmigoCloudSample
{
    partial class AmigoCloudSampleForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.EmailLabel = new System.Windows.Forms.Label();
            this.ProjectLabel = new System.Windows.Forms.Label();
            this.PasswordLabel = new System.Windows.Forms.Label();
            this.LoginGroupBox = new System.Windows.Forms.GroupBox();
            this.LoginButton = new System.Windows.Forms.Button();
            this.PasswordTextBox = new System.Windows.Forms.TextBox();
            this.EmailTextBox = new System.Windows.Forms.TextBox();
            this.SelectDatasetGroupBox = new System.Windows.Forms.GroupBox();
            this.DatasetsComboBox = new System.Windows.Forms.ComboBox();
            this.label1 = new System.Windows.Forms.Label();
            this.ProjectsComboBox = new System.Windows.Forms.ComboBox();
            this.DatasetDataGridView = new System.Windows.Forms.DataGridView();
            this.LoginGroupBox.SuspendLayout();
            this.SelectDatasetGroupBox.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.DatasetDataGridView)).BeginInit();
            this.SuspendLayout();
            // 
            // EmailLabel
            // 
            this.EmailLabel.Location = new System.Drawing.Point(6, 25);
            this.EmailLabel.Name = "EmailLabel";
            this.EmailLabel.Size = new System.Drawing.Size(70, 20);
            this.EmailLabel.TabIndex = 0;
            this.EmailLabel.Text = "Email:";
            // 
            // ProjectLabel
            // 
            this.ProjectLabel.Location = new System.Drawing.Point(6, 22);
            this.ProjectLabel.Name = "ProjectLabel";
            this.ProjectLabel.Size = new System.Drawing.Size(70, 18);
            this.ProjectLabel.TabIndex = 3;
            this.ProjectLabel.Text = "Project";
            // 
            // PasswordLabel
            // 
            this.PasswordLabel.Location = new System.Drawing.Point(6, 49);
            this.PasswordLabel.Name = "PasswordLabel";
            this.PasswordLabel.Size = new System.Drawing.Size(70, 20);
            this.PasswordLabel.TabIndex = 4;
            this.PasswordLabel.Text = "Password: ";
            // 
            // LoginGroupBox
            // 
            this.LoginGroupBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.LoginGroupBox.Controls.Add(this.LoginButton);
            this.LoginGroupBox.Controls.Add(this.PasswordTextBox);
            this.LoginGroupBox.Controls.Add(this.EmailTextBox);
            this.LoginGroupBox.Controls.Add(this.EmailLabel);
            this.LoginGroupBox.Controls.Add(this.PasswordLabel);
            this.LoginGroupBox.Location = new System.Drawing.Point(12, 12);
            this.LoginGroupBox.Name = "LoginGroupBox";
            this.LoginGroupBox.Size = new System.Drawing.Size(753, 108);
            this.LoginGroupBox.TabIndex = 5;
            this.LoginGroupBox.TabStop = false;
            this.LoginGroupBox.Text = "Login";
            // 
            // LoginButton
            // 
            this.LoginButton.Anchor = System.Windows.Forms.AnchorStyles.Bottom;
            this.LoginButton.Location = new System.Drawing.Point(351, 72);
            this.LoginButton.Name = "LoginButton";
            this.LoginButton.Size = new System.Drawing.Size(75, 23);
            this.LoginButton.TabIndex = 8;
            this.LoginButton.Text = "Login";
            this.LoginButton.UseVisualStyleBackColor = true;
            this.LoginButton.Click += new System.EventHandler(this.LoginButton_Click);
            // 
            // PasswordTextBox
            // 
            this.PasswordTextBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.PasswordTextBox.Location = new System.Drawing.Point(82, 46);
            this.PasswordTextBox.Name = "PasswordTextBox";
            this.PasswordTextBox.PasswordChar = '*';
            this.PasswordTextBox.Size = new System.Drawing.Size(652, 20);
            this.PasswordTextBox.TabIndex = 6;
            // 
            // EmailTextBox
            // 
            this.EmailTextBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.EmailTextBox.Location = new System.Drawing.Point(82, 22);
            this.EmailTextBox.Name = "EmailTextBox";
            this.EmailTextBox.Size = new System.Drawing.Size(652, 20);
            this.EmailTextBox.TabIndex = 5;
            // 
            // SelectDatasetGroupBox
            // 
            this.SelectDatasetGroupBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.SelectDatasetGroupBox.Controls.Add(this.DatasetsComboBox);
            this.SelectDatasetGroupBox.Controls.Add(this.label1);
            this.SelectDatasetGroupBox.Controls.Add(this.ProjectsComboBox);
            this.SelectDatasetGroupBox.Controls.Add(this.ProjectLabel);
            this.SelectDatasetGroupBox.Enabled = false;
            this.SelectDatasetGroupBox.Location = new System.Drawing.Point(12, 135);
            this.SelectDatasetGroupBox.Name = "SelectDatasetGroupBox";
            this.SelectDatasetGroupBox.Size = new System.Drawing.Size(753, 84);
            this.SelectDatasetGroupBox.TabIndex = 9;
            this.SelectDatasetGroupBox.TabStop = false;
            this.SelectDatasetGroupBox.Text = "Select Dataset";
            // 
            // DatasetsComboBox
            // 
            this.DatasetsComboBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.DatasetsComboBox.FormattingEnabled = true;
            this.DatasetsComboBox.Location = new System.Drawing.Point(82, 51);
            this.DatasetsComboBox.Name = "DatasetsComboBox";
            this.DatasetsComboBox.Size = new System.Drawing.Size(652, 21);
            this.DatasetsComboBox.TabIndex = 12;
            this.DatasetsComboBox.SelectedIndexChanged += new System.EventHandler(this.DatasetsComboBox_SelectedIndexChanged);
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(6, 51);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(70, 18);
            this.label1.TabIndex = 11;
            this.label1.Text = "Dataset";
            // 
            // ProjectsComboBox
            // 
            this.ProjectsComboBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.ProjectsComboBox.FormattingEnabled = true;
            this.ProjectsComboBox.Location = new System.Drawing.Point(82, 19);
            this.ProjectsComboBox.Name = "ProjectsComboBox";
            this.ProjectsComboBox.Size = new System.Drawing.Size(652, 21);
            this.ProjectsComboBox.TabIndex = 10;
            this.ProjectsComboBox.SelectedIndexChanged += new System.EventHandler(this.ProjectsComboBox_SelectedIndexChanged);
            // 
            // DatasetDataGridView
            // 
            this.DatasetDataGridView.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.DatasetDataGridView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.DatasetDataGridView.Location = new System.Drawing.Point(12, 236);
            this.DatasetDataGridView.Name = "DatasetDataGridView";
            this.DatasetDataGridView.Size = new System.Drawing.Size(753, 281);
            this.DatasetDataGridView.TabIndex = 10;
            // 
            // AmigoCloudSampleForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(777, 529);
            this.Controls.Add(this.DatasetDataGridView);
            this.Controls.Add(this.SelectDatasetGroupBox);
            this.Controls.Add(this.LoginGroupBox);
            this.Name = "AmigoCloudSampleForm";
            this.ShowIcon = false;
            this.SizeGripStyle = System.Windows.Forms.SizeGripStyle.Show;
            this.Text = "AmigoCloud Sample";
            this.LoginGroupBox.ResumeLayout(false);
            this.LoginGroupBox.PerformLayout();
            this.SelectDatasetGroupBox.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.DatasetDataGridView)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Label EmailLabel;
        private System.Windows.Forms.Label ProjectLabel;
        private System.Windows.Forms.Label PasswordLabel;
        private System.Windows.Forms.GroupBox LoginGroupBox;
        private System.Windows.Forms.TextBox EmailTextBox;
        private System.Windows.Forms.TextBox PasswordTextBox;
        private System.Windows.Forms.Button LoginButton;
        private System.Windows.Forms.GroupBox SelectDatasetGroupBox;
        private System.Windows.Forms.ComboBox DatasetsComboBox;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.ComboBox ProjectsComboBox;
        private System.Windows.Forms.DataGridView DatasetDataGridView;
    }
}

