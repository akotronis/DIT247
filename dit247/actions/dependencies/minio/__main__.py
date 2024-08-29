def main(params):
    firstname, lastname = map(lambda x:params.get(x, 'stranger'), ['firstname', 'lastname'])
    greeting = f'Hello {firstname} - {lastname}'
    return {"greeting": greeting}