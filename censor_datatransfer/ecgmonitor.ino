import com.scichart.charting.visuals.annotations.AnnotationBase;
import com.scichart.charting.visuals.annotations.HorizontalLineAnnotation;
import com.scichart.charting.visuals.annotations.VerticalLineAnnotation;
import com.scichart.charting.visuals.axes.AutoRange;
import com.scichart.charting.visuals.axes.NumericAxis;
import com.scichart.charting.visuals.renderableSeries.FastLineRenderableSeries;
import com.scichart.charting.visuals.renderableSeries.IRenderableSeries;
import com.scichart.charting.visuals.series.XyDataSeries;
import com.scichart.core.framework.UpdateSuspender;
import com.scichart.core.model.DoubleValues;
import com.scichart.examples.utils.ItemSelectedListener;
import com.scichart.examples.utils.ViewExtensions;

import java.util.Collections;
import java.util.Date;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Spinner;

import java.util.ArrayList;
import java.util.List;
import java.util.Collections;
import java.util.Calendar;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;

import butterknife.BindView;

public class ECGmonitor extends ExampleBaseFragment {
    private final static long TIME_INTERVAL = 80; // 80ms

    private final IxydataSeries<Double, Double> ecgDataSeries = new XyDataSeries<>(Date.class, Double.class);


}
