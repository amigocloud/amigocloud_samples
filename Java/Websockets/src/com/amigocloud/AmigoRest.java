package com.amigocloud;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.conn.ClientConnectionManager;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.conn.tsccm.ThreadSafeClientConnManager;
import org.apache.http.params.HttpParams;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class AmigoRest {

	private static DefaultHttpClient getThreadSafeClient() {
		DefaultHttpClient client = new DefaultHttpClient();
		ClientConnectionManager mgr = client.getConnectionManager();
		HttpParams params = client.getParams();
		client = new DefaultHttpClient(new ThreadSafeClientConnManager(params, mgr.getSchemeRegistry()), params);
		return client;
	}

	private HttpClient httpclient = getThreadSafeClient();

	private String apiToken;

	public AmigoRest(String token) {
		apiToken = token;
	}

	public String get(String url) {
		String uri;
		uri = url + "?token=" + apiToken;
		HttpGet httpget = new HttpGet(uri);
		try {
			HttpResponse response = httpclient.execute(httpget);

			BufferedReader rd = new BufferedReader(
					new InputStreamReader(response.getEntity().getContent()));

			StringBuffer result = new StringBuffer();
			String line = "";
			while ((line = rd.readLine()) != null) {
				result.append(line);
			}

			return result.toString();
		} catch (Exception e) {
			e.printStackTrace();
		}
		return null;
	}

}
