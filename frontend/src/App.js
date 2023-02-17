import React, { useState, useEffect } from 'react'
import Search from './pages/Search/Search';


function App() {
    const [data, setData] = useState([{}])
    const [word, setWord] = useState('');

    useEffect(() => {
        fetch("/hello").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                console.log(data)
            }
        )
    }, [])

    return (
        <div>
            {(typeof data.message === 'undefined') ? (
                <p>Loading...</p>
            ) : (
                <p>{data.message}</p>
            )}

            <Search word={word} setWord={setWord} />
        </div>
    )
}

export default App