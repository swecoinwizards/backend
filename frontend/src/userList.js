import React, { useState, useEffect } from 'react'

function UserList() {
    const [data, setData] = useState([{}])

    useEffect(() => {
        fetch("/users/list").then(
            res => res.json()
        ).then(
            data => {
                setData(JSON.stringify(data).split())
            }            
        )
    }, [])

    return (
        <div>
            {Object.values(data[0])}
        </div>
    )
}

export default UserList
