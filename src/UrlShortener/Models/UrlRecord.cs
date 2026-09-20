namespace UrlShortener.Models;

public class UrlRecord
{
    public int Id { get; set; }
    public string ShortCode { get; set; } = string.Empty;
    public string LongUrl { get; set; } = string.Empty;
    public int AccessCount { get; set; }
}