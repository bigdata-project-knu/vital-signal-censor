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

    @GET("/censor/user1")
    fun censor(
        @Query("query") jsonParams : String
    ) : Call<List<Double>>

    @GET("/censor/user1")
    fun predict(
        @Query("query") jsonParams : String
    ) : Call<List<Double>>

    companion object{
        private const val BASE_URL = "http://10.0.2.2:8000" //백엔드 서버
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
