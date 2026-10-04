function StudentProfile() {
  return (
    <div style={{ padding: "2rem" }}>
      <h2>Student Profile</h2>
      <form>
        <div>
          <label>Full Name</label>
          <input type="text" placeholder="Enter your name" />
        </div>
        <div>
          <label>Preferred Role</label>
          <input type="text" placeholder="e.g. Developer" />
        </div>
        <div>
          <label>Technical Skills</label>
          <input type="text" placeholder="e.g. Python, React" />
        </div>
        <button type="submit">Save Profile</button>
      </form>
    </div>
  );
}

export default StudentProfile;