package com.example.bigdata_prj

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.navigation.fragment.NavHostFragment
import androidx.navigation.ui.NavigationUI
import com.example.bigdata_prj.databinding.ActivityAppMainBinding

class AppMain : AppCompatActivity() {
    private lateinit var mBinding : ActivityAppMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

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
