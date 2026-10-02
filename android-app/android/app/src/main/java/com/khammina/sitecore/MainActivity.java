package com.khammina.sitecore;

import android.os.Bundle;
import android.webkit.WebSettings;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Let the page's <meta name="viewport"> set the display scale (SiteCore "Display size", default 90%).
        // Pinch-zoom stays locked by the page (minimum-scale = maximum-scale); no on-screen zoom buttons.
        WebSettings s = this.bridge.getWebView().getSettings();
        s.setUseWideViewPort(true);
        s.setLoadWithOverviewMode(true);
        s.setSupportZoom(true);
        s.setBuiltInZoomControls(true);
        s.setDisplayZoomControls(false);
    }
}
