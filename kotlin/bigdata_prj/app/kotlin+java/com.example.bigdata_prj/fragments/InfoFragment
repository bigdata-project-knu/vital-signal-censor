package com.example.bigdata_prj.fragments

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.example.bigdata_prj.databinding.FragmentInfoBinding

class InfoFragment : Fragment() {
    private var mBinding : FragmentInfoBinding? = null

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val binding = FragmentInfoBinding.inflate(inflater, container, false)
        mBinding = binding

        mBinding?.infoFragmentTitle?.text = "OOO님 안녕하세요"
        mBinding?.infoFragmentText?.text = "사용자 정보\n\n문의하기\n\n앱 정보"


        return mBinding?.root
    }

    override fun onDestroyView() {
        mBinding = null
        super.onDestroyView()
    }
}
