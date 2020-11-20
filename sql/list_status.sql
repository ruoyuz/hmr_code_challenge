-- list number of subscriptions in each status --
SELECT current_status, COUNT(current_status)
FROM public.itunes_subscription
GROUP BY current_status;

