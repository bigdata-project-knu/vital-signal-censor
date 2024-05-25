package com.example.bigdata_prj

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitObject {
    // http 넣기
    private const val URL = ""

    private val client = Retrofit
        .Builder()
        .baseUrl(URL)
        .addConverterFactory(GsonConverterFactory.create()).build()

    fun getInstance():Retrofit{
        return client
    }
}
