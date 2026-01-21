import React, { useState, useEffect} from "react";
import { useParams, useNavigate, Link } from "react-router-dom";

function BlogDetail({user}) {
    const { id } = useParams();
    const navigate = useNavigate();
    const [blog, setBlog] = useState(null);
    const [comments, setComments] = useState([]);
    const [newComment, setNewComment] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchBlogAndComments();
    }, [id]);

    function fetchBlogAndComments() {
        setIsLoading(true);
        setError(null);

        fetch(`/server/blogs/${id}`)
            .then((r) => {
                if (!r.ok) {
                    throw new Error("Blog not found")
                }
                return r.json();
            })
            .then((blogData) => {
                setBlog(blogData);
                return fetchComments();
            })
            .catch((err) => {
                console.error("Error fetching blog.", err);
                setError(err.message);
                setIsLoading(false);
            });
    }

    function fetchComments() {
        fetch(`/server/comments?blog_id=${id}`)
            .then((r) => {
                if(!r.ok) {
                    throw new Error("Error fetching comments")
                }
                return r.json()
            })
            .then((data) => {
                setComments(data);
                setIsLoading(false);
            })
            .catch((err) => {
                console.error("Error fetching comments", err)
                setError("Failed to load comments")
                setIsLoading(false)
            });
    }

    function handleCommentSubmit(e) {
        e.preventDefault();
        if(!newComment.trim()) {
            setError("Comment cannot be empty");
            return;
        }

        setIsSubmitting(true);
        setError(null)

        fetch("/server/comments", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                comment: newComment,
                blog_id: parseInt(id)
            }),
        })
        .then((r) => {
            if(!r.ok) {
                return r.json().then(err => {
                    throw new Error(err.error || "Failed to post Comment");
                });
            }
            return r.json();
        })
        .then((newCommentData) => {
            setComments([...comments, newCommentData]);
            setNewComment("");
            setIsSubmitting(false);
        })
        .catch((err) => {
            console.error("Error posting comment", err);
            setError(err.message);
            setIsSubmitting(false);
        });
    }

    function handleDeleteBlog() {
        if(!window.confirm("Are you sure you want to delete this blog?")) {
            return;
        }

        fetch(`/server/blogs/${id}`, {
            method: "DELETE",
        })
            .then((r) => {
                if(!r.ok) {
                    throw new Error("Failed to delete blog");
                }
                navigate("/")
            })
            .catch((err) => {
                console.error("Error deleting blog", err);
                setError("Failed to delete blog");
            });
    }

    function handleDeleteComment(commentId) {
        if(!window.confirm("Are you sure you want to delete this comment?")) {
            return;
        }

        fetch(`/server/comments/${commentId}`, {
            method: "DELETE",
        })
            .then((r) => {
                if(!r.ok) {
                    throw new Error("Failed to delete comment");
                }
                setComments(comments.filter(c => c.id !== commentId));
            })
            .catch((err) => {
                console.error("Error deleting comment", err);
                setError("Failed to delete comment");
            });
        }
        if (isLoading) {
            return <div>Loading...</div>;
        }
        if (error && !blog) {
            return (
                <div>
                    <p>Error: {error}</p>
                    <Link to="/">Back to Home</Link>
                </div>
            )
        }
        if (!blog) {
            return <div>Blog not found</div>
        }

        return (
            <div className="blog-detail">
                <nav>
                    <Link to="/">Back to Home</Link>
                </nav>
                {error && (
                    <div className="error-message">
                        <p>{error}</p>
                        <button onClick={() => setError(null)}>Dismiss</button>
                    </div>
                )}

                <article className="blog-content">
                    <h1>{blog.title}</h1>
                    <div className="blog-meta">
                        <span>{blog.username}</span>
                    </div>
                    <div className="blog-body">
                        <p>{blog.body_text}</p>
                    </div>
                    {blog.url && (
                        <div className="blog-source">
                            <a href={blog.url} target="_blank">Read orignal article</a>
                        </div>
                    )}

                    {blog.user_id === user.id && (
                        <div className="blog-actions">
                            <Link to={`/blogs/${id}/edit`}>
                                <button>Edit</button>
                            </Link>
                            <button onClick={handleDeleteBlog}>Delete</button>
                        </div>
                    )}
                </article>

                <section className="comments-section">
                    <h2>Comments ({comments.length})</h2>

                    <form onSubmit={handleCommentSubmit} className="comment-form">
                        <textarea
                            value={newComment}
                            onChange={(e) => setNewComment(e.target.value)}
                            placeholder="Write a comment..."
                            rows="3"
                        />
                        <button type="submit" disabled={isSubmitting}>
                            {isSubmitting ? "Posting" : "Post comment"}
                        </button>
                    </form>

                    <div className="comments-list">
                        {comments.length === 0 ? (
                            <p>No comments yet</p>
                        ) : (
                            comments.map((comment) => (
                                <div key={comment.id} className="comment">
                                    <div className="comment-header">
                                        <strong>{comment.username}</strong>
                                        {comment.user_id === user.id && (
                                            <button onClick={() => handleDeleteComment(comment.id)} className="delete-comment">Delete</button>
                                        )}
                                    </div>
                                    <p>{comment.comment}</p>
                                </div>
                            ))
                        )}
                    </div>
                </section>
            </div>
        )
};

export default BlogDetail;