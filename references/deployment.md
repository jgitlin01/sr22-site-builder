# Validation and deployment

## Validate first

`scripts/validate.py <site-root> <geo-root>` gates on:

1. **Leftover template variables** — `$slug`, `{name}` that never got substituted. Ships
   as visible garbage.
2. **Invalid JSON-LD** — one trailing comma and the whole block is ignored by Google,
   silently. You get zero schema and no error anywhere.
3. **Broken internal links / missing images** — resolve every root-relative `href`/`src`
   against the filesystem.
4. **Missing structural tags** — truncated writes.

Fix everything before uploading. A bad substitution caught locally is a re-run; caught
after deploy it's a re-upload plus whatever Google crawled in between.

## Deploying over FTP

**Parallelize.** Sequential upload of ~90 files runs several minutes and will blow past
most command timeouts. 8–12 parallel connections is a good range:

```bash
find <geo-root> -name index.html | xargs -P 12 -I{} \
  curl -sS --user "$CRED" -T "{}" "ftp://$HOST/{}"
```

**Create remote directories serially first.** Parallel `--ftp-create-dirs` racing on the
same new directory produces `curl: (9) Server denied you to change to the given
directory` across most of the batch. Upload one file into the new directory by itself
first, then run the parallel batch:

```bash
curl -sS --user "$CRED" --ftp-create-dirs -T <one-file> "ftp://$HOST/<dir>/<one-file>"
find ... | xargs -P 12 ...   # rest of batch
```

**Upload images before pages** so nothing 404s in the window between.

## CDN caching — the one that will confuse you

Managed hosts (Hostinger, etc.) put a CDN in front of the origin. That cache can pin a
**stale or truncated** response for a specific URL indefinitely, even after you upload a
correct file.

The signature: one URL renders blank/garbled while its source file on disk is perfect,
and the same URL **with a query string** (`?x=1`) renders fine. That's diagnostic — a
query string bypasses the cached entry. If you see that, purge the CDN cache
(hPanel → Dashboard → Cache → Clear cache, or the host's equivalent) before you start
debugging HTML you already know is correct.

Also note `curl` may get a bot-check interstitial from the CDN where a real browser gets
the page. Verify final rendering in an actual browser, not just curl.

## Verify live

Pull every URL from the sitemap and confirm 200s. From the browser console on the live
origin (avoids CORS):

```js
fetch('/sitemap.xml').then(r=>r.text()).then(t=>{
  const urls=[...t.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m=>m[1]);
  return Promise.all(urls.map(u=>fetch(u,{cache:'no-store'}).then(r=>[u,r.status])))
    .then(rs=>JSON.stringify(rs.filter(x=>x[1]!==200)));
});
```

Then look at 2–3 real pages in a browser. Automated checks confirm the pages exist;
only your eyes confirm they look right.

## After launch

- Submit `sitemap.xml` in Google Search Console — far faster than waiting for organic
  discovery of ~90 new URLs.
- If the client has a Google Business Profile, the city page for their home city is the
  natural landing page for it.
- Rotate any temporary deploy credentials created during the build.
- Real reviews are the highest-value future addition: they unlock legitimate
  `AggregateRating` schema, which none of these pages can carry until the reviews exist.
