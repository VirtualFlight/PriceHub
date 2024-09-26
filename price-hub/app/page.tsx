'use client'

import React from 'react'
import {useState, useEffect} from 'react'

export default function page() {
  const [test, setTest] = useState([])
  
  useEffect(()=>{
    testing()
  },[])

  const testing = async() => {
    const response = await fetch("http://127.0.0.1:8080/test")
    const data = await response.json()
    setTest(data)
    console.log(data)
  }
  
  
  return (
    <div>yourmom</div>
  )
}



