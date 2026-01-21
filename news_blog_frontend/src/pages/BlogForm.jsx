import React, { useState, useEffect } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";

function BlogForm({ user }) {
    const { id } = useParams();
    const navigate = useNavigate();
    const isEditMode = Boolean(id);

    const [formData, setFormData] = useState({
        title: "",
        body_text: "",
        url: ""
    });
    const [errors, setErrors] = useState([])
    const [isLoading, setIsLoading] = useState(false)
    const [isFetching, setIsFetching] = useState(isEditMode)

    useEffect(() => {
        if (isEditMode) {
            fetchBlog();
        }
    }, [id]);

    function fetchBlog() {
        setIsFetching(true);
        fetch(`/server/blogs/${id}`)
            .then((r) => {
                if(!r.ok) {
                    throw new Error("Failed to fetch blog");
                }
                return r.json()
            })
            .then((blog) => {
                setFormData({
                    title: blog.title,
                    body_text: blog.body_text,
                    url: blog.url
                });
                setIsFetching(false)
            })
            .catch((err) => {
                console.error("Error fetching blog", err)
                setErrors([err.message])
                setIsFetching(false)
            });
    }
    
    function handleChange(e) {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    }

    function handleSubmit(e) {
        e.preventDefault();
        setErrors([]);
        setIsLoading(true);

        const url = isEditMode ? `/server/blogs/${id}` : `/server/blogs`;
        const method = isEditMode ? "PATCH" : "POST";

        fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formData)
        })
        .then((r) => {
            if(!r.ok){
                return r.json().then((err) => {
                    throw new Error(err.error || "Failed to save blog")
                })
            }
            return r.json()
        })
        .then((blog) => {
            navigate(`/blogs/${blog.id}`);
        })
        .catch((err) => {
            console.error("Error saving blog", err);
            setErrors([err.message]);
            setIsLoading(false);
        })
    }
    
    if (isFetching) {
        return <div>Loading...</div>;
    }

    return (
        <div className="blog-form-container">
            <nav>
                <Link to="/">Back to Home</Link>
            </nav>
            <h1>{isEditMode ? "Edit blog post" : "Create new blog post"}</h1>
            <form onSubmit={handleSubmit} className="blog-form">
                <div className="form-group">
                    <label htmlFor="title">Title</label>
                    <input
                        type="text"
                        id="title"
                        name="title"
                        value={formData.title}
                        onChange={handleChange}
                        placeholder="Enter blog title, max 100 characters"
                        maxLength="100"
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="body_text">Body</label>
                    <textarea
                        id="body_text"
                        name="body_text"
                        value={formData.body_text}
                        onChange={handleChange}
                        placeholder="Enter body text here, minimum 50 characters"
                        rows="10"
                        required
                    />
                    <small>{formData.body_text.length} characters</small>
                </div>

                <div className="form-group">
                    <label htmlFor="url">Source Link</label>
                    <input
                        type="url"
                        id="url"
                        name="url"
                        value={formData.url}
                        onChange={handleChange}
                        placeholder="https://example.com/article"
                        required
                    />
                </div>

                {errors.length > 0 && (
                    <div className="error-messages">
                        {errors.map((err, index) => (
                            <p key={index}>{err}</p>
                        ))}
                    </div>
                )}

                <div className="form-actions">
                    <button type="submit" disabled={isLoading}>
                        {isLoading ? "Saving..." : isEditMode ? "Update Post" : "Create new post"}
                    </button>
                    <button type="button" onClick={() => navigate(isEditMode ? `/blogs/${id}` : "/")}>Cancel</button>
                </div>
            </form>
        </div>
    );
}

export default BlogForm
