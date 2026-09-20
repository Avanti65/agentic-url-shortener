using System.Net;
using System.Net.Http.Json;
using Microsoft.AspNetCore.Mvc.Testing;
using NUnit.Framework;

namespace UrlShortener.Tests;

public class UrlShortenerTests
{
    private WebApplicationFactory<Program> _factory;
    private HttpClient _client;

    [SetUp]
    public void Setup()
    {
        _factory = new WebApplicationFactory<Program>();

        // Disable auto-redirect so we can explicitly verify the 302 Found response
        _client = _factory.CreateClient(new WebApplicationFactoryClientOptions
        {
            AllowAutoRedirect = false
        });
    }

    [TearDown]
    public void TearDown()
    {
        _client.Dispose();
        _factory.Dispose();
    }

    [Test]
    public async Task CreateShortUrl_ReturnsSuccessAndEightCharacterCode()
    {
        var response = await _client.PostAsJsonAsync("/shorten", new { Url = "https://example.com" });
        var result = await response.Content.ReadFromJsonAsync<ShortenResult>();

        Assert.That(response.StatusCode, Is.EqualTo(HttpStatusCode.OK));
        Assert.That(result, Is.Not.Null);
        Assert.That(result!.ShortCode.Length, Is.EqualTo(8));
    }

    [Test]
    public async Task FollowRedirect_WithValidCode_Returns302Found()
    {
        var setupResponse = await _client.PostAsJsonAsync("/shorten", new { Url = "https://google.com" });
        var setupResult = await setupResponse.Content.ReadFromJsonAsync<ShortenResult>();

        var redirectResponse = await _client.GetAsync($"/{setupResult!.ShortCode}");

        Assert.That(redirectResponse.StatusCode, Is.EqualTo(HttpStatusCode.Found));
    }

    [Test]
    public async Task GetAnalytics_AfterClick_ReturnsAccessCountOne()
    {
        var setupResponse = await _client.PostAsJsonAsync("/shorten", new { Url = "https://github.com" });
        var setupResult = await setupResponse.Content.ReadFromJsonAsync<ShortenResult>();
        await _client.GetAsync($"/{setupResult!.ShortCode}");

        var analyticsResponse = await _client.GetAsync($"/analytics/{setupResult.ShortCode}");
        var analytics = await analyticsResponse.Content.ReadFromJsonAsync<AnalyticsResult>();

        Assert.That(analyticsResponse.StatusCode, Is.EqualTo(HttpStatusCode.OK));
        Assert.That(analytics!.LongUrl, Is.EqualTo("https://github.com"));
        Assert.That(analytics.AccessCount, Is.EqualTo(1));
    }

    private class ShortenResult { public string ShortCode { get; set; } = string.Empty; }
    private class AnalyticsResult { public string LongUrl { get; set; } = string.Empty; public int AccessCount { get; set; } }
}