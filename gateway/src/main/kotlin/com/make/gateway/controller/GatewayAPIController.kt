package com.make.gateway.controller

import org.springframework.beans.factory.annotation.Value
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RestController
import java.io.BufferedReader
import java.io.InputStreamReader

@RestController
class GatewayAPIController {

    @Value("\${file.path}")
    val filePath: String = ""

    @PostMapping("/make/{target}")
    fun execMakeTarget(@PathVariable("target") target: String): String{
        val command: String = "make -f "+filePath+" "+target
        println(command)
        val process: Process = Runtime.getRuntime().exec(command)
        process.waitFor()
        val bufferReader = BufferedReader(InputStreamReader(process.inputStream))
        println(bufferReader.readLine())
        if(process.exitValue()==0)
            return "Successfully Executed"
        return "Failed to Execute Makefile"
    }
}