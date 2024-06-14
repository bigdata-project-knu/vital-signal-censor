package com.example.bigdata_prj.fragments

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.example.bigdata_prj.databinding.FragmentHomeBinding

class HomeFragment : Fragment() {

    private var mBinding : FragmentHomeBinding? = null

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val binding = FragmentHomeBinding.inflate(inflater, container, false)
        mBinding = binding

        mBinding?.homeFragmentTitle?.text = "홈"
        mBinding?.homeFragmentText?.text = "인공지능을 활용한\n" +
                "IoT 생체신호 감지 모듈 개발\n\n\n프로젝트 참여\n위혜정\n유동훈\n이진욱"


        return mBinding?.root
    }

    override fun onDestroyView() {
        mBinding = null
        super.onDestroyView()
    }
}
