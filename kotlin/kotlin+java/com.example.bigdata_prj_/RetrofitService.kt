package com.example.bigdata_prj

import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Path

interface RetrofitService {
    @GET("posts/1")
    suspend fun getPost1() : POST

    @GET("posts/{number}")
    suspend fun getPostNumber(
        @Path("number") number : Int
    ) : POST
}
