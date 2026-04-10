-- Execute this in your Supabase SQL Editor
-- Make sure to run this line below if you ALREADY ran the old script to add the new column:
ALTER TABLE email_logs ADD COLUMN IF NOT EXISTS request_id UUID DEFAULT gen_random_uuid() NOT NULL;

CREATE TABLE IF NOT EXISTS email_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    request_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    event_name TEXT NOT NULL,
    recipient_email TEXT NOT NULL,
    subject TEXT NOT NULL,
    status TEXT NOT NULL,
    error_details TEXT
);

-- Optional: Add Row Level Security (RLS) if you want to restrict dashboard access,
-- but since this is an internal log, you can leave it disabled or restrict to service role.
ALTER TABLE email_logs ENABLE ROW LEVEL SECURITY;

-- Allow insert access to authenticated/service roles
DROP POLICY IF EXISTS "Allow service role to insert logs" ON email_logs;
CREATE POLICY "Allow service role to insert logs" ON email_logs
    FOR INSERT 
    WITH CHECK (true);

-- Allow reading logs for admins/service roles
DROP POLICY IF EXISTS "Allow service role to select logs" ON email_logs;
CREATE POLICY "Allow service role to select logs" ON email_logs
    FOR SELECT
    USING (true);
