import pandas as pd

def clean_data(file_path: str) -> pd.DataFrame:
    """
    Reads the project CSV file, applies standard cleaning steps,
    and returns a cleaned DataFrame.

    Parameters
    ----------
    file_path : str
        Path to the raw CSV file.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame ready for analysis.
    """

    # Read the CSV file
    df = pd.read_csv(file_path)

    # Refine column names
    df.columns = (
        df.columns
        .str.strip()           # remove extra spaces
        .str.lower()           # lowercase all names
        .str.replace(' ', '_') # replace spaces with underscores
        .str.replace('-', '_') # replace dashes with underscores
        .str.replace('?', '')  # remove question marks
    )

    # Handle missing values
    df['issue'] = df['issue'].fillna('Unknown')
    df['sub_issue'] = df['sub_issue'].fillna('Unknown')
    df['company_public_response'] = df['company_public_response'].fillna('Unknown')
    df['state'] = df['state'].fillna('Unknown')
    df['tags'] = df['tags'].fillna('').apply(lambda x: x.split(',') if isinstance(x, str) else [])
    df['consumer_disputed'] = df['consumer_disputed'].fillna('No')
    df['consumer_complaint_narrative'] = df['consumer_complaint_narrative'].fillna('Not provided')

    # Remove redacted characters (For example, "XXX")
    df['consumer_complaint_narrative'] = df['consumer_complaint_narrative'].str.replace(r'X+', '', regex=True)

    # Normalize string by collapsing all whitespace (spaces, tabs, newlines) into single spaces
    df['consumer_complaint_narrative'] = df['consumer_complaint_narrative'].str.split().str.join(" ")

    # Drop unnecessary columns
    df = df.drop(
        columns=[
            'tags',
            'submitted_via',
            'consumer_consent_provided',
            'timely_response',
            'consumer_disputed'
        ],
        errors='ignore'  # in case some columns don't exist
    )

    return df