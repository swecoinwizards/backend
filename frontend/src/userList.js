import React, { useState, useEffect } from 'react'

function UserList() {
    const [data, setData] = useState([{}])

    useEffect(() => {
        fetch("/users/list").then(
            res => res.json()
        ).then(
            data => {
                setData(JSON.stringify(data))
                console.log(JSON.stringify(data))
            }            
        )
    }, [])
    
    return (
        <div>
            <p>{JSON.stringify(data)}</p>
        </div>
    )
}

export default UserList
