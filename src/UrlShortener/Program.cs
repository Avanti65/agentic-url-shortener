using Microsoft.EntityFrameworkCore;
using UrlShortener.Data;
using UrlShortener.Endpoints;

var builder = WebApplication.CreateBuilder(args);

//Configure Entity Framework Core with SQLite using the connection string from appsettings.json
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
builder.Services.AddDbContext<AppDbContext>(options => options.UseSqlite(connectionString));

var app = builder.Build();

// Ensure database is created on startup
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.EnsureCreated();
}

// Register endpoints
app.MapUrlEndpoints();

app.Run();

public partial class Program { }