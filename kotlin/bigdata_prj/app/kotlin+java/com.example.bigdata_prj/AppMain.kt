package com.example.bigdata_prj

import android.os.Bundle
import android.util.Log
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.navigation.findNavController
import androidx.navigation.fragment.NavHostFragment
import androidx.navigation.ui.NavigationUI
import com.example.bigdata_prj.databinding.ActivityAppMainBinding
import com.example.bigdata_prj.fragments.DataFragment
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class AppMain : AppCompatActivity() {
    private lateinit var mBinding : ActivityAppMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        val retrofitservice = RetrofitService.create()

        val currentDataCall = retrofitservice.censor("censor")
        val predictDataCall = retrofitservice.predict("predict")

        var currentDataArray: DoubleArray? = null
        var predictDataArray: DoubleArray? = null

        currentDataCall.enqueue(object : Callback<Array<Double>>{
            override fun onResponse(call: Call<Array<Double>>, response: Response<Array<Double>>) {
                if(response.isSuccessful){
                    val currentData = response.body()
                    currentDataArray = currentData?.toDoubleArray()
                    currentDataArray?.forEach { value ->
                        Log.d("censor", value.toString())
                    }
                    if(currentDataArray != null && predictDataArray != null){
                        navigateToDataFragment(currentDataArray!!, predictDataArray!!)
                    }
                }
                else{
                    Log.d("Fail", "currentDataCall")
                }
            }
            override fun onFailure(call: Call<Array<Double>>, t: Throwable) {
                Log.d("Fail", "${t.message}")
            }
        })
        predictDataCall.enqueue(object : Callback<Array<Double>>{
            override fun onResponse(call: Call<Array<Double>>, response: Response<Array<Double>>) {
                if(response.isSuccessful){
                    val predictData = response.body()
                    predictDataArray = predictData?.toDoubleArray()
                    predictDataArray?.forEach { value ->
                        Log.d("censor", value.toString())
                    }
                    if(currentDataArray != null && predictDataArray != null){
                        navigateToDataFragment(currentDataArray!!, predictDataArray!!)
                    }
                }
                else{
                    Log.d("Fail", "predictDataCall")
                }
            }
            override fun onFailure(call: Call<Array<Double>>, t: Throwable) {
                Log.d("Fail", "${t.message}")
            }
        })

        mBinding = ActivityAppMainBinding.inflate(layoutInflater)
        setContentView(mBinding.root)

        val navHostFragment = supportFragmentManager.findFragmentById(R.id.my_nav_host) as NavHostFragment
        val navController = navHostFragment.navController
        NavigationUI.setupWithNavController(mBinding.myBottomNav, navController)
    }


    private fun navigateToDataFragment(currentData: DoubleArray, predictData: DoubleArray) {
        val bundle = Bundle().apply {
            putDoubleArray("currentData", currentData)
            putDoubleArray("predictData", predictData)
        }

        val navController = findNavController(R.id.my_nav_host)
        navController.navigate(R.id.dataFragment, bundle)
    }
}
