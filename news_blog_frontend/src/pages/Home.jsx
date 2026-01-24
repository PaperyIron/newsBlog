import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

function Home({ user, onLogout }) {
    const [blogs, setBlogs] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const navigate = useNavigate();

    useEffect(() => {
        fetchBlogs(currentPage);
    }, [currentPage]);

    function fetchBlogs(page = 1) {
        setIsLoading(true);
        setError(null);
        fetch(`/server/blogs?page=${page}&per_page=10`)
            .then((r) => {
                if (!r.ok) {
                    throw new Error('Failed to fetch blogs');
                }
                return r.json();
            })
            .then((data) => {
                setBlogs(data.blogs);
                setTotalPages(data.pages);
                setIsLoading(false);
            })
            .catch((error) => {
                console.error("Error fetching blogs:", error);
                setError("Failed to load blogs. Please try again.");
                setIsLoading(false);
            });
    }

    function handleLogout() {
        fetch("/server/logout", {
            method: "DELETE",
        })
            .then((r) => {
                if (r.ok) {
                    onLogout();
                    navigate("/login");
                } else {
                    setError("Failed to logout. Please try again.");
                }
            })
            .catch((error) => {
                console.error("Error logging out:", error);
                setError("Failed to logout. Please try again.");
            });
    }

    function handleRefresh() {
        fetchBlogs(currentPage);
    }

    if (isLoading && blogs.length === 0) {
        return <div>Loading blogs...</div>;
    }

    return (
        <div className="home">
            <header className="home-header">
                <h1>News Blog</h1>
                <div className="user-info">
                    <p>Welcome, {user.username}!</p>
                    <button onClick={handleLogout}>Logout</button>
                </div>
            </header>

            {error && (
                <div className="error-message">
                    <p>{error}</p>
                    <button onClick={() => setError(null)}>Dismiss</button>
                </div>
            )}

            <div className="blog-actions">
                <Link to="/blogs/new">
                    <button>Create New Post</button>
                </Link>
                <button onClick={handleRefresh} disabled={isLoading}>
                    {isLoading ? "Refreshing..." : "Refresh"}
                </button>
            </div>

            <div className="all-blogs-list">
                {blogs.length === 0 ? (
                    <p>No blog posts. Be the first to create one!</p>
                ) : (
                    blogs.map((blog) => (
                        <div key={blog.id} className="blog-card">
                            <h2>
                                <Link to={`/blogs/${blog.id}`}>{blog.title}</Link>
                            </h2>
                            <p className="blog-preview">
                                {blog.body_text.substring(0, 150)}
                                {blog.body_text.length > 150 && "..."}
                            </p>
                            {blog.url && (
                                <a 
                                    href={blog.url} 
                                    target="_blank" 
                                    rel="noopener noreferrer"
                                >
                                    Read the article
                                </a>
                            )}
                            <div className="blog-meta">
                                <span>By {blog.username}</span>
                            </div>
                        </div>
                    ))
                )}
            </div>

            {totalPages > 1 && (
                <div className="pagination">
                    <button 
                        onClick={() => setCurrentPage(currentPage - 1)} 
                        disabled={currentPage === 1 || isLoading}
                    >
                        Previous
                    </button>
                    <span>Page {currentPage} of {totalPages}</span>
                    <button 
                        onClick={() => setCurrentPage(currentPage + 1)} 
                        disabled={currentPage === totalPages || isLoading}
                    >
                        Next
                    </button>
                </div>
            )}
        </div>
    );
}

export default Home;
