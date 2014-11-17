package com.amigocloud.amigomobile.locator;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.provider.Settings;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class LocatorActivity extends Activity {


	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main);


		final View loginContainer = findViewById(R.id.login_container);
		final View serviceContainer = findViewById(R.id.service_container);
		final Button serviceButton = (Button) findViewById(R.id.service_button);

		if(LocationService.isRunnning()) {
			loginContainer.setVisibility(View.GONE);
			serviceContainer.setVisibility(View.VISIBLE);
			serviceButton.setText("Stop Location Broadcast");
		}

		final TextView deviceId = (TextView) findViewById(R.id.device_id_text);
		deviceId.setText(Settings.Secure.getString(getContentResolver() ,Settings.Secure.ANDROID_ID));
		final TextView userId = (TextView) findViewById(R.id.user_id_text);
		final TextView projectId = (TextView) findViewById(R.id.project_id_text);
		final TextView datasetId = (TextView) findViewById(R.id.dataset_id_text);

		serviceButton.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View view) {
				if(LocationService.isRunnning()) {
					stopService(new Intent(LocatorActivity.this, LocationService.class));
					serviceButton.setText("Start Location Broadcast");
				} else {
					LocationService.setIds(deviceId.getText().toString(),
										   Long.parseLong(userId.getText().toString()),
										   Long.parseLong(projectId.getText().toString()),
									       Long.parseLong(datasetId.getText().toString()));
					startService(new Intent(LocatorActivity.this, LocationService.class));
					serviceButton.setText("Stop Location Broadcast");
				}
			}
		});
		final TextView email = (TextView) findViewById(R.id.email_text);
		final TextView password = (TextView) findViewById(R.id.password_text);
		final Button loginButton = (Button) findViewById(R.id.login_button);
		loginButton.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View view) {
				LocatorApplication.runOnNetworkThread(new Runnable() {
					@Override
					public void run() {
						final boolean success = LocatorApplication.getRestClient().login(email.getText().toString(), password.getText().toString());
						runOnUiThread(new Runnable() {
							@Override
							public void run() {
								if (success) {
									loginContainer.setVisibility(View.GONE);
									serviceContainer.setVisibility(View.VISIBLE);
									InputMethodManager imm = (InputMethodManager)getSystemService(Context.INPUT_METHOD_SERVICE);
									if(imm != null)
										imm.hideSoftInputFromWindow(loginButton.getWindowToken(), 0);
								} else {
									Toast.makeText(LocatorActivity.this, "Login Failed", Toast.LENGTH_SHORT).show();
								}
							}
						});

					}
				});
			}
		});
	}
}
