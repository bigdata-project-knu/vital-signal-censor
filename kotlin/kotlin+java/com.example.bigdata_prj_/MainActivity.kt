package com.example.bigdata_prj

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
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

        val button = findViewById<Button>(R.id.button)
        button.setOnClickListener {
            val intent = Intent(this, AppMain::class.java)
            startActivity(intent)
            //startActivity(Intent(this, MainScreen::class.java))
            val editText = findViewById<EditText>(R.id.editTextText)
            val editText2 = findViewById<EditText>(R.id.editTextTextPassword)

            var textId = editText.text.toString()
            var textPw = editText2.text.toString()
            val retrofitInstance =
                RetrofitObject.getInstance().create(RetrofitService::class.java)


            CoroutineScope(Dispatchers.Main).launch {
                try {
                    val result = withContext(Dispatchers.IO) {
                        retrofitInstance.getPost1()
                    }
                } catch (e: Exception) {
                    onFailure(e)
                }
            }
        }
    }

    private fun onFailure(t: Throwable) {
        var dialog = AlertDialog.Builder(this@MainActivity)
        dialog.setTitle("로그인 실패")
        dialog.setMessage("로그인에 실패하였습니다")
        dialog.show()
    }

    private fun onResponse(response: Post) {
        var dialog = AlertDialog.Builder(this@MainActivity)
        dialog.setTitle("로그인 성공")
        dialog.setMessage("로그인에 성공하였습니다")
        dialog.show()
        startActivity(Intent(this, AppMain::class.java))
    }
}
