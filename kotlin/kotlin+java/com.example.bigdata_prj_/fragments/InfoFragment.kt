package com.example.bigdata_prj.fragments

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.example.bigdata_prj.databinding.FragmentDataBinding
import com.example.bigdata_prj.databinding.FragmentHomeBinding

class DataFragment : Fragment() {

    private var mBinding : FragmentDataBinding? = null

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val binding = FragmentDataBinding.inflate(inflater, container, false)
        mBinding = binding
        return mBinding?.root
    }

    override fun onDestroyView() {
        mBinding = null
        super.onDestroyView()
    }
}
