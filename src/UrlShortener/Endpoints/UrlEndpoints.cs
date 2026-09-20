using Microsoft.EntityFrameworkCore;
using UrlShortener.Data;
using UrlShortener.Models;

namespace UrlShortener.Endpoints;

public static class UrlEndpoints
{
    public static void MapUrlEndpoints(this WebApplication app)
    {
        // POST /shorten
        app.MapPost("/shorten", async (AppDbContext db, ShortenRequest request) =>
        {
            if (string.IsNullOrWhiteSpace(request.Url)) return Results.BadRequest("URL is required.");

            var shortCode = Guid.NewGuid().ToString("N").Substring(0, 8);
            var record = new UrlRecord { ShortCode = shortCode, LongUrl = request.Url, AccessCount = 0 };

            db.UrlRecords.Add(record);
            await db.SaveChangesAsync();

            return Results.Ok(new { ShortCode = shortCode });
        });

        // GET /{code}
        app.MapGet("/{code}", async (AppDbContext db, string code) =>
        {
            var record = await db.UrlRecords.FirstOrDefaultAsync(r => r.ShortCode == code);
            if (record == null) return Results.NotFound();

            record.AccessCount++;
            await db.SaveChangesAsync();

            return Results.Redirect(record.LongUrl);
        });

        // GET /analytics/{code}
        app.MapGet("/analytics/{code}", async (AppDbContext db, string code) =>
        {
            var record = await db.UrlRecords.FirstOrDefaultAsync(r => r.ShortCode == code);
            if (record == null) return Results.NotFound();

            return Results.Ok(new { record.LongUrl, record.AccessCount });
        });
    }
}