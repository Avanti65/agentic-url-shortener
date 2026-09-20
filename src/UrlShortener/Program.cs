using Microsoft.EntityFrameworkCore;
using UrlShortener.Data;
using UrlShortener.Endpoints;

var builder = WebApplication.CreateBuilder(args);

// Configure Entity Framework Core with SQLite using the connection string from appsettings.json
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

namespace UrlShortener.Data
{
    public class ShortUrl
    {
        public int Id { get; set; }
        public string OriginalUrl { get; set; } = string.Empty;
        public string ShortCode { get; set; } = string.Empty;
        public string? CustomAlias { get; set; }
        public DateTime CreatedOn { get; set; } = DateTime.UtcNow;
    }

    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

        public DbSet<ShortUrl> ShortUrls => Set<ShortUrl>();

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<ShortUrl>()
                .HasIndex(u => u.ShortCode)
                .IsUnique();

            modelBuilder.Entity<ShortUrl>()
                .HasIndex(u => u.CustomAlias)
                .IsUnique();
        }
    }
}

namespace UrlShortener.Endpoints
{
    using System;
    using System.Linq;
    using System.Text.RegularExpressions;
    using Microsoft.AspNetCore.Builder;
    using Microsoft.AspNetCore.Http;
    using Microsoft.AspNetCore.Routing;
    using Microsoft.EntityFrameworkCore;
    using UrlShortener.Data;

    public static class UrlEndpoints
    {
        public static void MapUrlEndpoints(this IEndpointRouteBuilder routes)
        {
            routes.MapPost("/api/shorten", async (ShortenRequest request, AppDbContext db, HttpContext httpContext) =>
            {
                if (string.IsNullOrWhiteSpace(request.OriginalUrl) || !Uri.TryCreate(request.OriginalUrl, UriKind.Absolute, out _))
                {
                    return Results.BadRequest("A valid absolute original URL is required.");
                }

                string? customAlias = null;
                if (!string.IsNullOrWhiteSpace(request.CustomAlias))
                {
                    customAlias = request.CustomAlias.Trim();

                    // Validation: Length 3-30 characters
                    if (customAlias.Length < 3 || customAlias.Length > 30)
                    {
                        return Results.BadRequest("Custom alias must be between 3 and 30 characters.");
                    }

                    // Validation: Format (alphanumeric, hyphens, and underscores only)
                    if (!Regex.IsMatch(customAlias, "^[a-zA-Z0-9_\\-]+$"))
                    {
                        return Results.BadRequest("Custom alias can only contain alphanumeric characters, hyphens, and underscores.");
                    }

                    // Validation: Uniqueness (check against both existing custom aliases and short codes to prevent collisions)
                    var aliasExists = await db.ShortUrls.AnyAsync(u => u.CustomAlias == customAlias || u.ShortCode == customAlias);
                    if (aliasExists)
                    {
                        return Results.Conflict("The custom alias is already in use.");
                    }
                }

                // Generate a unique short code
                string shortCode;
                do
                {
                    shortCode = GenerateShortCode();
                }
                while (await db.ShortUrls.AnyAsync(u => u.ShortCode == shortCode || u.CustomAlias == shortCode));

                var shortUrl = new ShortUrl
                {
                    OriginalUrl = request.OriginalUrl,
                    ShortCode = shortCode,
                    CustomAlias = customAlias
                };

                db.ShortUrls.Add(shortUrl);
                await db.SaveChangesAsync();

                var scheme = httpContext.Request.Scheme;
                var host = httpContext.Request.Host;
                var identifier = customAlias ?? shortCode;
                var shortenedUrl = $"{scheme}://{host}/{identifier}";

                return Results.Created($"/{identifier}", new ShortenResponse(shortenedUrl, shortCode, customAlias));
            });

            routes.MapGet("/{codeOrAlias}", async (string codeOrAlias, AppDbContext db) =>
            {
                var shortUrl = await db.ShortUrls
                    .FirstOrDefaultAsync(u => u.ShortCode == codeOrAlias || u.CustomAlias == codeOrAlias);

                if (shortUrl == null)
                {
                    return Results.NotFound("Short URL not found.");
                }

                return Results.Redirect(shortUrl.OriginalUrl);
            });
        }

        private static string GenerateShortCode()
        {
            const string chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
            return string.Create(7, chars, (span, state) =>
            {
                for (int i = 0; i < span.Length; i++)
                {
                    span[i] = state[Random.Shared.Next(state.Length)];
                }
            });
        }
    }

    public record ShortenRequest(string OriginalUrl, string? CustomAlias = null);
    public record ShortenResponse(string ShortenedUrl, string ShortCode, string? CustomAlias);
}