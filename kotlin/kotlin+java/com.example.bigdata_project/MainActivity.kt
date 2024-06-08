//retrofit 연결 전 확인용

package com.example.bigdata_project

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.bigdata_project.R
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

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

        val editText = findViewById<EditText>(R.id.editTextText)
        val editText2 = findViewById<EditText>(R.id.editTextTextPassword)

        val button = findViewById<Button>(R.id.button)
        button.setOnClickListener {
            var id = editText.text.toString()
            var pw = editText2.text.toString()

            //val retrofitservice = RetrofitService.create() 미리보기용
            //val data = UserModel(id, pw)

            //미리보기용
            val intent = Intent(this@MainActivity, AppMain::class.java)
            startActivity(intent)
            finish()
            //미리보기용

//            retrofitservice.requestLogin(data).enqueue(object : Callback<LoginDTO> {
//                override fun onResponse(
//                    call: Call<LoginDTO>,
//                    response: Response<LoginDTO>
//                ) {
//                    Log.d("로그인 통신 성공", response.toString())
//                    Log.d("로그인 통신 성공", response.body().toString())
//
//                    when (response.code()) {
//                        200 -> {
//                            var dialog = AlertDialog.Builder(this@MainActivity)
//                            dialog.setTitle("로그인 성공")
//                            dialog.setMessage("로그인에 성공하였습니다")
//                            dialog.show()
//                            val intent = Intent(this@MainActivity, AppMain::class.java)
//                            startActivity(intent)
//                            finish()
//                        }
//
//                        405 -> {
//                            Toast.makeText(
//                                this@MainActivity,
//                                "로그인 실패 : 아이디 혹은 비밀번호가 올바르지 않습니다",
//                                Toast.LENGTH_LONG
//                            ).show()
//                            var dialog = AlertDialog.Builder(this@MainActivity)
//                            dialog.setTitle("로그인 실패")
//                            dialog.setMessage("로그인에 실패하였습니다")
//                            dialog.show()
//                        }
//
//                        500 -> {
//                            Toast.makeText(this@MainActivity, "로그인 실패 : 서버 오류", Toast.LENGTH_LONG)
//                                .show()
//                            var dialog = AlertDialog.Builder(this@MainActivity)
//                            dialog.setTitle("로그인 실패")
//                            dialog.setMessage("로그인에 실패하였습니다")
//                            dialog.show()
//                        }
//                    }
//                }
//
//                override fun onFailure(call: Call<LoginDTO>, t: Throwable) {
//                    Log.d("로그인 통신 실패", t.message.toString())
//                    Log.d("로그인 통신 실패", "fail")
//                    var dialog = AlertDialog.Builder(this@MainActivity)
//                    dialog.setTitle("로그인 실패")
//                    dialog.setMessage("로그인에 실패하였습니다")
//                    dialog.show()
//                }
//            })
        }
    }
}
