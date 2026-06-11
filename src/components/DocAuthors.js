/* eslint-disable react/prop-types */
import React from 'react';

export default function DocAuthors({ authors }) {
    if (authors && authors.length > 0) {
        var authorLabel = "Author";
        if (authors.length > 1) {
            authorLabel = "Authors"
        }
        return (
            <div>
                <span className="docAuthorLabel">{authorLabel + ':'} </span>
                {
                    authors.map((author, i) => {
                        var name = author.name;
                        var email = author.email;
                        var key = email + String(i) + (Math.random() + 1).toString(36);
                        return (<span key={key} className="docAuthor"><a href={'https://aus.delve.office.com/?p=' + email + '&v=work'} target='_blank' rel="nofollow noreferrer">{name}</a></span>);
                    })
                }
            </div>
        );
    } else {
        return null;
    }
}


