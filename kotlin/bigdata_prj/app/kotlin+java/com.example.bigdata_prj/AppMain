package com.example.bigdata_prj

import android.os.Bundle
import android.util.Log
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.navigation.fragment.NavHostFragment
import androidx.navigation.ui.NavigationUI
import com.example.bigdata_prj.databinding.ActivityAppMainBinding
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class AppMain : AppCompatActivity() {
    private lateinit var mBinding : ActivityAppMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        val retrofitservice = RetrofitService.create()

        retrofitservice.censor("censor").enqueue(object : Callback<List<Double>>{
            override fun onResponse(call: Call<List<Double>>, response: Response<List<Double>>) {
                if(response.isSuccessful.not()){
                    Log.d("Fail", "NoCheck")
                    return
                }
                val currentData = response.body()
                currentData?.forEach {value ->
                    Log.d("censor", value.toString())
                }
            }

            override fun onFailure(call: Call<List<Double>>, t: Throwable) {
                Log.d("Fail", "Fail: ${t.message}")
            }
        })

        retrofitservice.predict("censor").enqueue(object : Callback<List<Double>>{
            override fun onResponse(call: Call<List<Double>>, response: Response<List<Double>>) {
                if(response.isSuccessful.not()){
                    Log.d("Fail", "NoCheck")
                    return
                }
                val predictData = response.body()
                predictData?.forEach {value ->
                    Log.d("predict", value.toString())
                }
            }

            override fun onFailure(call: Call<List<Double>>, t: Throwable) {
                Log.d("Fail", "Fail: ${t.message}")
            }
        })



        mBinding = ActivityAppMainBinding.inflate(layoutInflater)

        setContentView(mBinding.root)

        //네비게이션 담는 호스트
        val navHostFragment = supportFragmentManager.findFragmentById(R.id.my_nav_host) as NavHostFragment

        //네비게이션 컨트롤러
        val navController = navHostFragment.navController

        //bottom 네비게이션 뷰와 네비게이션 묶기
        NavigationUI.setupWithNavController(mBinding.myBottomNav, navController)
    }
}
