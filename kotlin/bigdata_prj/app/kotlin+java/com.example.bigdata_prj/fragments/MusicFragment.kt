package com.example.bigdata_prj.fragments

import android.net.Uri
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.VideoView
import androidx.fragment.app.Fragment
import com.example.bigdata_prj.R
import com.example.bigdata_prj.databinding.FragmentHomeBinding
import com.example.bigdata_prj.databinding.FragmentMusicBinding

class MusicFragment : Fragment() {

    private var mBinding : FragmentMusicBinding? = null

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val binding = FragmentMusicBinding.inflate(inflater, container, false)
        mBinding = binding

        mBinding?.musicFragmentTitle?.text = "잘 때 들으면 좋은 소리"

        mBinding?.startButton?.setOnClickListener{
            mBinding?.screenVideoView?.setVideoURI(Uri.parse("android.resource://com.example.bigdata_prj/"+R.raw.music1))
            mBinding?.screenVideoView?.start()
        }
        mBinding?.endButton?.setOnClickListener{
            mBinding?.screenVideoView?.stopPlayback()
        }
        return mBinding?.root
    }

    override fun onDestroyView() {
        mBinding = null
        super.onDestroyView()
    }
}
