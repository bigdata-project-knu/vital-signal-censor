package com.example.bigdata_prj

import com.google.gson.Gson
import com.google.gson.GsonBuilder
import retrofit2.Call
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query

interface RetrofitService {
    @FormUrlEncoded
    @POST("/login")
    fun requestLogin(
        @Body jsonParams : UserModel,
    ) : Call<LoginDTO>

    companion object{
        private const val BASE_URL = "" //백엔드 서버
        val gson : Gson = GsonBuilder().setLenient().create()

        fun create(): RetrofitService{
            return Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
                .create(RetrofitService::class.java)
        }

    }
}
