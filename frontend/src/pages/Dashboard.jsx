const fakeStudents = [
  { name: "Aarav Sharma", role: "Developer", skills: "Python, Java" },
  { name: "Ananya Patil", role: "UI/UX Designer", skills: "Figma, React" },
  { name: "Rohan Kulkarni", role: "Data Analyst", skills: "Python, SQL" },
];

function Dashboard() {
  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h2 style={{ color: "#2F5597" }}>Student Dashboard</h2>
      <table style={{ borderCollapse: "collapse", width: "100%", marginTop: "1rem" }}>
        <thead>
          <tr style={{ backgroundColor: "#2F5597", color: "white" }}>
            <th style={{ padding: "10px", textAlign: "left" }}>Name</th>
            <th style={{ padding: "10px", textAlign: "left" }}>Role</th>
            <th style={{ padding: "10px", textAlign: "left" }}>Skills</th>
          </tr>
        </thead>
        <tbody>
          {fakeStudents.map((s, i) => (
            <tr key={i} style={{ backgroundColor: i % 2 === 0 ? "#f2f2f2" : "white" }}>
              <td style={{ padding: "10px" }}>{s.name}</td>
              <td style={{ padding: "10px" }}>{s.role}</td>
              <td style={{ padding: "10px" }}>{s.skills}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Dashboard;