import openai
res = openai.Completion.create(
    model="davinci:ft-replicated:dexter-test-sbct-2023-02-08-02-59-22",
    prompt="write a support bundle yaml to collect logs has selector dd=rr in namespace sayhi->")

print(res["choices"][0]["text"])