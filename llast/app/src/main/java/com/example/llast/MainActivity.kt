package com.example.llast

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import android.view.View
import android.widget.Button
import androidx.fragment.app.FragmentManager
import androidx.fragment.app.FragmentTransaction
import com.example.llast.fragments.AnotherFragment
import com.example.llast.fragments.LeftFragment
import com.example.llast.fragments.RightFragment

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
        // leftButton을 참조하는 코드
        val leftButton = findViewById<Button>(R.id.leftButton)
// 클릭 리스너 등록 또는 다른 동작 수행
        leftButton.setOnClickListener {
            supportFragmentManager.beginTransaction()
                .replace(R.id.fragment_container, LeftFragment())
                .addToBackStack(null)
                .commit()
        }
        // leftButton을 참조하는 코드
        val rightButton = findViewById<Button>(R.id.rightButton)
// 클릭 리스너 등록 또는 다른 동작 수행
        // 오른쪽 버튼 클릭 시 RightFragment로 이동
        rightButton.setOnClickListener {
            supportFragmentManager.beginTransaction()
                .replace(R.id.fragment_container, RightFragment())
                .addToBackStack(null)
                .commit()
        }
    }
    //back 버튼 구현
    fun onBackButtonClick(view: View) {
        supportFragmentManager.popBackStack()
    }

    fun onButtonClick(view: View) {
        // Fragment를 교체하는 코드를 작성합니다.
        val fragment = AnotherFragment() // 이동할 Fragment의 인스턴스를 생성합니다.
        val fragmentManager: FragmentManager = supportFragmentManager
        val fragmentTransaction: FragmentTransaction = fragmentManager.beginTransaction()
        fragmentTransaction.replace(R.id.fragment_container, fragment)
        fragmentTransaction.addToBackStack(null)
        fragmentTransaction.commit()
    }

}