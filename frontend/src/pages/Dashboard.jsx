// TODO: Replace fakeStudents with a real fetch() call to the /students API once Esha's backend endpoint is ready
const fakeStudents = [
  { name: "Aarav Sharma", role: "Developer", skills: "Python, Java" },
  { name: "Ananya Patil", role: "UI/UX Designer", skills: "Figma, React" },
  { name: "Rohan Kulkarni", role: "Data Analyst", skills: "Python, SQL" },
];

function Dashboard() {
  return (
    <div style={{ padding: "2rem" }}>
      <h2>Student Dashboard</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Name</th>
            <th>Role</th>
            <th>Skills</th>
          </tr>
        </thead>
        <tbody>
          {fakeStudents.map((s, i) => (
            <tr key={i}>
              <td>{s.name}</td>
              <td>{s.role}</td>
              <td>{s.skills}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Dashboard;