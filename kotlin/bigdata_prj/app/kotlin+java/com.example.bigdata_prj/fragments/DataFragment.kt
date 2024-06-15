package com.example.bigdata_prj.fragments

import android.graphics.Color
import android.graphics.Typeface
import android.icu.text.SimpleDateFormat
import android.icu.util.Calendar
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.navArgs
import com.example.bigdata_prj.R
import com.example.bigdata_prj.databinding.FragmentDataBinding
import com.example.bigdata_prj.databinding.FragmentHomeBinding
import com.github.mikephil.charting.charts.LineChart
import com.github.mikephil.charting.components.XAxis
import com.github.mikephil.charting.data.Entry
import com.github.mikephil.charting.data.LineData
import com.github.mikephil.charting.data.LineDataSet
import com.github.mikephil.charting.formatter.IndexAxisValueFormatter
import java.util.Locale

class DataFragment : Fragment() {

    private var mBinding : FragmentDataBinding? = null
    private lateinit var lineChart: LineChart

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val binding = FragmentDataBinding.inflate(inflater, container, false)
        mBinding = binding

        mBinding?.dataFragmentTitle?.text = "수면 데이터 분석"
        mBinding?.dataAnalysis?.text = "지난 수면 시간 동안\nO번 수면 무호흡증이 일어났습니다.\n\n다시 수면을 취하면\nO번 수면 무호흡증이 예상됩니다."
        val currentData = arguments?.getDoubleArray("currentData")
        val predictData = arguments?.getDoubleArray("predictData")

        lineChart = mBinding!!.root.findViewById(R.id.lineChart)

        val currentEntries = mutableListOf<Entry>()
        val predictEntries = mutableListOf<Entry>()

        if (currentData != null) {
            for (i in currentData.indices) {
                currentEntries.add(Entry(i.toFloat(), currentData[i].toFloat()))
            }
        }

        if (predictData != null) {
            val startIndex = currentData?.size ?: 0
            for (i in predictData.indices) {
                predictEntries.add(Entry((startIndex + i).toFloat(), predictData[i].toFloat()))
            }
        }

        val currentDataSet = LineDataSet(currentEntries, "센서값")
        currentDataSet.color = Color.WHITE
        currentDataSet.circleColors = listOf(Color.WHITE)
        currentDataSet.setDrawValues(false)
        currentDataSet.circleRadius = 1f
        currentDataSet.circleHoleColor = Color.TRANSPARENT

        val predictDataSet = LineDataSet(predictEntries, "예측값")
        predictDataSet.color = Color.GREEN
        predictDataSet.circleColors = listOf(Color.GREEN)
        predictDataSet.setDrawValues(false)
        predictDataSet.circleRadius = 1f
        predictDataSet.circleHoleColor = Color.TRANSPARENT

        val lineData = LineData(currentDataSet, predictDataSet)
        lineChart.data = lineData
        lineChart.legend.isEnabled = true

        val xAxis = lineChart.xAxis
        xAxis.position = XAxis.XAxisPosition.BOTTOM
        xAxis.granularity = 1f
        xAxis.setDrawGridLines(false)

        val timeEntries = mutableListOf<String>()
        timeEntries.add("")
        timeEntries.add("현재")
        timeEntries.add("")
        xAxis.valueFormatter = IndexAxisValueFormatter(timeEntries)

        val leftAxis = lineChart.axisLeft
        val rightAxis = lineChart.axisRight
        rightAxis.isEnabled = false
        lineChart.invalidate()

        return mBinding?.root
    }

    override fun onDestroyView() {
        mBinding = null
        super.onDestroyView()
    }
}
